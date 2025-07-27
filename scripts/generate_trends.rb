#!/usr/bin/env ruby
require "json"
require "yaml"
require "time"

ROOT = File.expand_path("..", __dir__)
prompts = Dir.glob("#{ROOT}/_reviewers/**/*.md")

LANG_MAP = {
  "javascript" => "JavaScript",
  "typescript" => "TypeScript",
  "json"       => "JSON",
  "yaml"       => "YAML",
  "toml"       => "TOML",
  "css"        => "CSS",
  "html"       => "HTML",
  "xml"        => "XML",
  "php"        => "PHP"
}

stats = {
  languages:      Hash.new(0),
  categories:     Hash.new(0),
  repositories:   Hash.new(0),
  comments_year:  Hash.new(0),
  comments_dow:   Hash.new(0),   # "Mon".."Sun"
  total_comments: 0,
  bot_comments:   0,
  suggestion_comments: 0,
  prompt_occ_bins: Hash.new(0)   # "1", "2-3", "4-7", "8+"
}

prompts.each do |file|
  content = File.read(file)
  parts = content.split(/^---\s*$/, 3)
  meta = parts.size >= 3 ? (YAML.safe_load(parts[1]) || {}) : {}

  slug = File.basename(file, '.md')
  json_path = File.join(File.dirname(file), "#{slug}.json")
  records = File.exist?(json_path) ? JSON.parse(File.read(json_path)) : []
  comments = records.flat_map { |r| r['discussion_comments'] || [] }

  lang  = (meta["language"] || "Other").strip
  lang  = LANG_MAP.fetch(lang.downcase, lang)
  cat   = (meta["label"]    || "Uncategorised").strip
  repo  = (meta["repository"] || "Unknown/Unknown").strip

  stats[:languages][lang]  += 1
  stats[:categories][cat]  += 1
  stats[:repositories][repo] += 1

  occ = records.length
  bin = case occ
        when 1 then "1"
        when 2..3 then "2-3"
        when 4..7 then "4-7"
        else "8+"
        end
  stats[:prompt_occ_bins][bin] += 1

  comments.each do |c|
    stats[:total_comments] += 1
    stats[:bot_comments]   += 1 if c["comment_author"]&.match?(/\b(bot|\[bot\])\b/i)
    stats[:suggestion_comments] += 1 if c["comment_body"]&.include?("```suggestion")
    t = Time.parse(c["comment_created_at"]) rescue next
    stats[:comments_year][t.year] += 1
    stats[:comments_dow][t.strftime("%a")] += 1
  end
end

stats[:human_comments] = stats[:total_comments] - stats[:bot_comments]
stats[:generated_at]   = Time.now.utc.iso8601

out = File.join(ROOT, "assets/data/trends.json")
File.write(out, JSON.pretty_generate(stats))
puts "Wrote #{out}"

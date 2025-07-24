#!/usr/bin/env ruby
require "json"
require "yaml"
require "time"

ROOT = File.expand_path("..", __dir__)
prompts = Dir.glob("#{ROOT}/_reviewers/**/*.md")

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
  fm, body = File.read(file).split(/^---\s*$/, 3)[1..2]
  meta = YAML.safe_load(fm)

  lang  = (meta["language"] || "Other").strip
  cat   = (meta["label"]    || "Uncategorised").strip
  repo  = (meta["repository"] || "Unknown/Unknown").strip

  stats[:languages][lang]  += 1
  stats[:categories][cat]  += 1
  stats[:repositories][repo] += 1

  examples = (meta["comments"] || [])
  occ = examples.size
  bin = case occ
        when 1 then "1"
        when 2..3 then "2-3"
        when 4..7 then "4-7"
        else "8+"
        end
  stats[:prompt_occ_bins][bin] += 1

  examples.each do |c|
    stats[:total_comments] += 1
    stats[:bot_comments]   += 1 if c["author"]&.match?(/\b(bot|\[bot\])\b/i)
    stats[:suggestion_comments] += 1 if c["body"]&.include?("```suggestion")
    t = Time.parse(c["created_at"]) rescue next
    stats[:comments_year][t.year] += 1
    stats[:comments_dow][t.strftime("%a")] += 1
  end
end

stats[:human_comments] = stats[:total_comments] - stats[:bot_comments]
stats[:generated_at]   = Time.now.utc.iso8601

out = File.join(ROOT, "assets/data/trends.json")
File.write(out, JSON.pretty_generate(stats))
puts "Wrote #{out}"

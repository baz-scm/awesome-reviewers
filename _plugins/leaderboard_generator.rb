require 'json'
require 'set'
require 'yaml'
require 'fileutils'

module Jekyll
  class LeaderboardGenerator < Generator
    safe true
    priority :high


    def generate(site)
      contributors = {}
      reviewer_meta = {}

      Dir.glob(File.join(site.source, '_reviewers', '*.md')) do |md_file|
        slug = File.basename(md_file, '.md')
        data = YAML.load_file(md_file)
        reviewer_meta[slug] = {
          'title' => data['title'],
          'repository' => data['repository']
        }
      end

      Dir.glob(File.join(site.source, '_reviewers', '*.json')) do |json_file|
        data = JSON.parse(File.read(json_file))
        entry_slug = File.basename(json_file, '.json')

        data.each do |discussion|
          next unless discussion['discussion_comments']
          discussion['discussion_comments'].each do |comment|
            user = comment['comment_author']
            next if user.nil? || user.include?('[bot]')

            repo = comment['repo_full_name'] || reviewer_meta.dig(entry_slug, 'repository')
            contributors[user] ||= {
              'entries' => Set.new,
              'repos' => Set.new,
              'comments' => Hash.new { |h, k| h[k] = [] }
            }
            contributors[user]['entries'] << entry_slug
            contributors[user]['repos'] << repo if repo
            body = comment['comment_body']
            contributors[user]['comments'][entry_slug] << body if body
          end
        end
      end

      leaderboard = contributors.map do |user, info|
        {
          'user' => user,
          'entries_count' => info['entries'].size,
          'repos_count' => info['repos'].size,
          'repos' => info['repos'].to_a
        }
      end

      leaderboard.sort_by! { |entry| -entry['entries_count'] }
      leaderboard = leaderboard.first(50)

      site.data['leaderboard'] = leaderboard

      contributors_data = {}
      contributors.each do |user, info|
        entries = info['entries'].map do |slug|
          {
            'slug' => slug,
            'title' => reviewer_meta.dig(slug, 'title')
          }
        end

        contributors_data[user] = {
          'repos' => info['repos'].to_a,
          'entries' => entries,
          'comments' => info['comments']
        }
      end

      site.data['contributors'] = contributors_data
      site.config['contributors_data'] = contributors_data
    end
  end
end

Jekyll::Hooks.register :site, :post_write do |site|
  data = site.config['contributors_data']
  next unless data
  dest_dir = File.join(site.dest, 'assets', 'data')
  FileUtils.mkdir_p(dest_dir)
  File.write(File.join(dest_dir, 'contributors.json'), JSON.pretty_generate(data))
end

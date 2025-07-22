require 'json'
require 'set'
require 'yaml'
require 'fileutils'
require 'net/http'
require 'uri'

module Jekyll
  class LeaderboardGenerator < Generator
    safe true
    priority :high

    def fetch_github_info(username)
      url = URI("https://api.github.com/users/#{username}")
      req = Net::HTTP::Get.new(url)
      token = ENV['GITHUB_TOKEN']
      req['Authorization'] = "Bearer #{token}" if token
      req['User-Agent'] = 'AwesomeReviewers'
      begin
        res = Net::HTTP.start(url.hostname, url.port, use_ssl: true) { |h| h.request(req) }
        return {} unless res.is_a?(Net::HTTPSuccess)
        data = JSON.parse(res.body)
        {
          'name' => data['name'],
          'bio' => data['bio'],
          'company' => data['company'],
          'location' => data['location']
        }
      rescue => e
        Jekyll.logger.warn("GitHub user fetch failed for #{username}: #{e.message}")
        {}
      end
    end

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
        leaderboard.each do |entry|
          user = entry['user']
          info = contributors[user]
          next unless info

          entries = info['entries'].map do |slug|
            {
              'slug' => slug,
              'title' => reviewer_meta.dig(slug, 'title')
            }
          end

          meta = fetch_github_info(user)

          contributors_data[user] = {
            'name' => meta['name'],
            'bio' => meta['bio'],
            'company' => meta['company'],
            'location' => meta['location'],
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

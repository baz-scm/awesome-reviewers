require 'json'
require 'set'

module Jekyll
  class LeaderboardGenerator < Generator
    safe true
    priority :high

    def generate(site)
      contributors = {}

      Dir.glob(File.join(site.source, '_reviewers', '*.json')) do |json_file|
        data = JSON.parse(File.read(json_file))
        entry_slug = File.basename(json_file, '.json')

        data.each do |discussion|
          next unless discussion['discussion_comments']
          discussion['discussion_comments'].each do |comment|
            user = comment['comment_author']
            next if user.nil? || user.include?('[bot]')

            repo = comment['repo_full_name'] || site.data.dig('reviewers', entry_slug, 'repository')
            contributors[user] ||= { 'entries' => Set.new, 'repos' => Set.new }
            contributors[user]['entries'] << entry_slug
            contributors[user]['repos'] << repo if repo
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
    end
  end
end

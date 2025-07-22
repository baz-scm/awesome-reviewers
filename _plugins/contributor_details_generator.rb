require 'json'
require 'set'

module Jekyll
  class ContributorDetailsGenerator < Generator
    safe true
    priority :high

    def generate(site)
      contributors = Hash.new { |h, k| h[k] = { 'repos' => Set.new, 'entries' => {}, 'comments' => Hash.new { |hh, kk| hh[kk] = [] } } }

      # Map reviewer slug to title and repository from collection docs
      metadata = {}
      if site.collections['reviewers']
        site.collections['reviewers'].docs.each do |doc|
          slug = doc.basename_without_ext
          metadata[slug] = {
            'title' => doc.data['title'],
            'repository' => doc.data['repository']
          }
        end
      end

      Dir.glob(File.join(site.source, '_reviewers', '*.json')) do |json_file|
        slug = File.basename(json_file, '.json')
        entry_meta = metadata[slug] || {}
        entry_title = entry_meta['title']
        default_repo = entry_meta['repository']

        JSON.parse(File.read(json_file)).each do |discussion|
          next unless discussion['discussion_comments']
          discussion['discussion_comments'].each do |comment|
            user = comment['comment_author']
            next if user.nil? || user.include?('[bot]')
            repo = comment['repo_full_name'] || default_repo
            body = comment['comment_body']
            info = contributors[user]
            info['repos'] << repo if repo
            info['entries'][slug] = entry_title if entry_title
            if body && !body.strip.empty?
              info['comments'][slug] << body
            end
          end
        end
      end

      result = {}
      contributors.each do |user, info|
        result[user] = {
          'repos' => info['repos'].to_a.sort,
          'entries' => info['entries'].map { |s, t| { 'slug' => s, 'title' => t } },
          'comments' => info['comments']
        }
      end

      site.data['contributors'] = result
    end
  end
end

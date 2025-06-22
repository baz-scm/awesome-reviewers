require 'yaml'

module Jekyll
  class ReviewerReader < Generator
    safe true
    priority :high

    def generate(site)
      reviewers_dir = File.join(site.source, 'reviewers')
      return unless Dir.exist?(reviewers_dir)

      # Clear existing reviewers
      site.collections['reviewers'].docs.clear if site.collections['reviewers']

      # Read all reviewer files
      read_reviewers(site, reviewers_dir)
    end

    private

    def read_reviewers(site, reviewers_dir)
      Dir.foreach(reviewers_dir) do |repo_folder|
        next if repo_folder == '.' || repo_folder == '..'

        repo_path = File.join(reviewers_dir, repo_folder)
        next unless File.directory?(repo_path)

        # Process each markdown file in the repository folder
        Dir.glob(File.join(repo_path, '*.md')).each do |file_path|
          process_reviewer_file(site, file_path, repo_folder)
        end
      end
    end

    def process_reviewer_file(site, file_path, repo_folder)
      content = File.read(file_path)

      # Parse front matter and content
      if content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m
        front_matter = YAML.safe_load($1)
        content_body = content[($1.size + $2.size)..-1]
      else
        # If no front matter, try to extract from content
        front_matter = extract_metadata_from_content(content)
        content_body = content
      end

      # Create document
      doc = Jekyll::Document.new(
        file_path,
        {
          site: site,
          collection: site.collections['reviewers']
        }
      )

      # Set document data
      doc.data.merge!(front_matter) if front_matter
      doc.data['repository'] ||= repo_folder
      doc.data['layout'] = 'reviewer'

      # Set content
      doc.content = content_body.strip

      # Generate URL-friendly slug
      filename = File.basename(file_path, '.md')
      doc.data['slug'] = Jekyll::Utils.slugify(filename)

      # Add to collection
      site.collections['reviewers'].docs << doc
    end

    def extract_metadata_from_content(content)
      metadata = {}
      lines = content.split("\n")

      # Try to extract title from first line if it's a heading
      if lines.first&.start_with?('#')
        metadata['title'] = lines.first.gsub(/^#+\s*/, '').strip
      end

      # Look for common patterns in content
      content.scan(/^(\w+):\s*(.+)$/i).each do |key, value|
        case key.downcase
        when 'title', 'description', 'repository', 'label', 'language'
          metadata[key.downcase] = value.strip
        when 'comments', 'comment_count', 'comments_count'
          metadata['comments_count'] = value.strip.to_i
        end
      end

      metadata
    end
  end
end
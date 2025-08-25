require 'json'
require 'time'

module ReviewerDates
  Jekyll::Hooks.register :documents, :pre_render do |doc|
    next unless doc.collection && doc.collection.label == 'reviewers'
    json_path = doc.path.sub(/\.md$/, '.json')
    next unless File.exist?(json_path)

    begin
      data = JSON.parse(File.read(json_path))
      timestamps = data.map { |entry| Time.parse(entry['created_at']) rescue nil }.compact
      doc.data['added'] = timestamps.min if timestamps.any?
    rescue StandardError
      # leave added unset if parsing fails
    end
  end
end

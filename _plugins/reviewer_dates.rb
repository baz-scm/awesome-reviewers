require 'time'

module ReviewerDates
  Jekyll::Hooks.register :documents, :pre_render do |doc|
    next unless doc.collection && doc.collection.label == 'reviewers'
    json_path = doc.path.sub(/\.md$/, '.json')
    next unless File.exist?(json_path)

    begin
      doc.data['added'] = File.mtime(json_path)
    rescue StandardError
      # leave added unset if retrieval fails
    end
  end
end

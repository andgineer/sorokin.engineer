require 'yaml'
tags = []
Dir.glob(File.join('_posts','*.md')).each do |file|
	yaml_s = File.read(file).split(/^---$/)[1]
	yaml_h = YAML.load(yaml_s)
	tags += yaml_h['tags']
end

tags.map(&:downcase).uniq.each do |tag|
	File.write File.join('tags', "#{tag}.html"), <<-EOF
---
layout: tagpage
tag: #{tag}
permalink: /tags/#{tag}
lang: en
---
	EOF

	File.write File.join('tags', "#{tag}.html"), <<-EOF
---
layout: tagpage
tag: #{tag}
permalink: /tags_ru/#{tag}
lang: ru
locale: ru_RU
---
	EOF

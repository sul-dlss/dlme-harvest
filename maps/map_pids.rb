require 'csv'
require 'fileutils'
require 'json'
require 'open-uri'

require 'colorize'
require 'mechanize'

harvard = %w(
  https://earthworks.stanford.edu/catalog?f%5Bdct_provenance_s%5D%5B%5D=Harvard&f%5Blayer_geom_type_s%5D%5B%5D=Raster&per_page=100&bbox=46.400757%2042.269179%2048.729858%2044.190082
)

stanford = %w(
  https://earthworks.stanford.edu/?bbox=46.400757+42.269179+48.729858+44.190082&f%5Bdct_provenance_s%5D%5B%5D=Stanford&f%5Blayer_geom_type_s%5D%5B%5D=Raster&per_page=100
)


@include_prefix = %w(
  harvard
  stanford
  princeton
)

@pids = []

@a = Mechanize.new

# def collectPid(pid)
#   prefix = pid.split('-')[0]
#   @pids << pid if @include_prefix.include? prefix
# end
#
# urls.each do |url|
#   @a.get(url) do |doc|
#     data = doc.css("//div.documentHeader")
#     data.each do |pid|
#       collectPid pid.attr('data-layer-id')
#     end
#
#   end
# end
#
# puts @pids


# @repos = %w(
# https://github.com/OpenGeoMetadata/edu.stanford.purl.git
# https://github.com/OpenGeoMetadata/edu.princeton.arks.git
# https://github.com/OpenGeoMetadata/edu.harvard.git
# )
#
# FileUtils.mkdir_p('work')
# FileUtils.cd('work')
#
# @repos.each do |repo|
#   `git clone #{repo}`
# end

# dirs = Dir.entries('work')
FileUtils.cd('../work')
#
harvard_layers   = JSON.parse(File.read('edu.harvard/layers.json'))
princeton_layers = JSON.parse(File.read('edu.princeton.arks/layers.json'))
stanford_layers  = JSON.parse(File.read('edu.stanford.purl/layers.json'))

def cache_remote(link)
  f = File.basename(URI.parse(link).path)
  FileUtils.cd('/Users/waynegraham/projects/dlme-metadata/maps/records/stanford', :verbose => true)

  unless File.file? f
    puts "Downloading file #{link} to ".yellow
    @a.get(link).save
  else
    puts "File exits (#{link})".green
  end
end

CSV.foreach('../maps/map-layer-ids.csv') do |row|
  prefix = row.first.split('-')[0]
  suffix = row.first.sub("#{prefix}-",'')

  if(prefix == 'harvard')
    suffix.gsub!(/-/, '_') unless suffix.nil?
    suffix.upcase!
    suffix.prepend('HARVARD.SDE2.')

    # path = "#{FileUtils.pwd}/edu.harvard/#{harvard_layers[suffix]}/fgdc.xml" if harvard_layers[suffix]
    # FileUtils.cp(path, "../maps/records/harvard/#{suffix}.fgdc.xml") if harvard_layers[suffix]
  end

  if(prefix == 'stanford')
    suffix.prepend('https://purl.stanford.edu/')
    suffix += '.mods'

    cache_remote(suffix)
  end

end

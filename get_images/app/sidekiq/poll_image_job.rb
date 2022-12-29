class PollImageJob
  include Sidekiq::Worker

  COMBINE_FILE = './result/combine_images.csv'

  def perform(number)
    file_name = "image_#{number}.jpg"
    image_dir = "./result/#{file_name}"

    tmp_file = Down.download('https://thispersondoesnotexist.com/image')

    image_size = FastImage.size(tmp_file)
    file_size = tmp_file.size

    File.open(image_dir, 'wb') { |f| f << tmp_file.read }

    image_dir = "./get_images/result/#{file_name}"

    open(COMBINE_FILE, 'a') do |f|
      f.puts "#{number + 1};#{image_dir};#{file_name};image/jpeg;#{file_size};#{image_size.join(';')}"
    end
  end
end

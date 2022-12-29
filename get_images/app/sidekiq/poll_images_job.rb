class PollImagesJob
  include Sidekiq::Job

  def perform(no_images)
    (1..no_images).each do |number|
      PollImageJob.perform_async(number)
    end
  end
end

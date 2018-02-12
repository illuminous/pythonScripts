import gdata.docs.service
import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()







class YoutubeClient:

  def __init__(self):

    self.yt_service = gdata.youtube.service.YouTubeService()



  def print_items(self, entry):

    print 'Video title: %s'% entry.media.title.text

    print 'Video published on: %s'% entry.published.text

    print 'Video description: %s'% entry.media.description.text

    print 'Video category: %s'% entry.media.category[0].text

    print 'Video tags: %s' % entry.media.keywords.text

    print 'Video flash player URL: %s'% entry.GetSwfUrl()

    print 'Video duration: %s'% entry.media.duration.seconds

    print '----------------------------------------'



  def get_items(self, feed):

   for entry in feed.entry:

       self.print_items(entry)



client = YoutubeClient()
client.get_items(client.yt_service.GetMostLinkedVideoFeed())

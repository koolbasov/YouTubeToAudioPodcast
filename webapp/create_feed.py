from feedgen.feed import FeedGenerator
import datetime

fg = FeedGenerator()
fe = fg.add_entry()
fe.load_extension('podcast')
fg.load_extension('podcast')

fg.title('YoutubToRSSforTests')
fg.language('en')
fg.link(href='/webapp/rss.xml')
fg.description("Lorem Ipsum is simply dummy ")
fg.pubDate(datetime.datetime(2024, 6, 20, 12, 32, 49, tzinfo=datetime.timezone.utc))
fg.lastBuildDate(datetime.datetime(2024, 7, 10, 7, 49, 41, 799575, tzinfo=datetime.timezone.utc))
fg.podcast.itunes_image('webapp/youtubetopodcast-cover.jpg')
fg.podcast.itunes_author('YoutubToRSSforTests')
fg.podcast.itunes_explicit('no')


fe.title('5 Great beginner Python Projects')
fe.link(href='https://www.youtube.com/watch?v=SrSl6T1My00')
fe.description("Sponsored by Kite")
fe.enclosure(url="webapp/podcasts/SrSl6T1My00.mp3", length="410.784", type="audio/mpeg")
fe.guid('PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f::SrSl6T1My00')
fe.pubDate(datetime.datetime(2020, 3, 13, 15, 42, 4, tzinfo=datetime.timezone.utc))
fe.author({'name': 'https://www.youtube.com/channel/UC68KSmHePPePCjW4v57VPQg', 'email': 'Python Programmer'})
fe.podcast.itunes_duration(int(410.784))

fg.rss_file('rss.xml')
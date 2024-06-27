from bs4 import BeautifulSoup

with open("PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f.xml", "r", encoding="utf-8") as f:
    playlist_xml = f.read()

with open("PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f.html", "r", encoding="utf-8") as f:
    playlist_html = f.read()

playlist_id = "PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"

fields_for_db = []

soup_html = BeautifulSoup(playlist_html, "html.parser")
soup_xml = BeautifulSoup(playlist_xml, "xml")
all_items = soup_xml.findAll("entry")

# Fields for feed
db_feed_id = "ADD WHEN ADDING TO THE DATABASE"
db_user_id = "ADD WHEN ADDING TO THE DATABASE"
feed_title = soup_html.find("meta", property="og:title")['content']
feed_link = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
db_language = "ADD WHEN ADDING TO THE DATABASE"
feed_description = soup_html.find("meta", property="og:description")['content']
feed_pubDate = "TODO"
lastBuildDate = "TODO"
feed_image = "IT WILL BE THE SAME STATIC IMAGE FOR ALL FEEDS"

feed_fields_for_db = dict(
    id=db_feed_id,
    user_id=db_user_id,
    feed_title=feed_title,
    feed_link=feed_link,
    language=db_language,
    feed_description=feed_description,
    feed_pubDate=feed_pubDate,
    lastBuildDate=lastBuildDate,
    feed_image=feed_image
)

fields_for_db.append(feed_fields_for_db)


for item in all_items:
    db_podcast_id = "ADD WHEN ADDING TO THE DATABASE"
    feed_id = "ADD WHEN ADDING TO THE DATABASE"
    ytb_podcast_id = item.find("yt:videoId").text
    podcast_title = item.find("title").text
    ytb_link = item.find("link")["href"]
    ytb_description = item.find("description").text
    enclosure = "TODO"
    guid = playlist_id + '::' + ytb_podcast_id
    pubDate = "TODO"
    ytb_author = item.find("author").text.strip()
    duration = "TODO"
    ytb_image = item.find("thumbnail")["url"]
    podcast_fields_for_db = dict(
        id=db_podcast_id,
        feed_id=feed_id,
        ytb_podcast_id=ytb_podcast_id,
        podcast_title=podcast_title,
        ytb_link=ytb_link,
        ytb_description=ytb_description,
        enclosure=enclosure,
        guid=guid,
        pubDate=pubDate,
        ytb_author=ytb_author,
        duration=duration,
        ytb_image=ytb_image
    )
    fields_for_db.append(podcast_fields_for_db)

print(fields_for_db)

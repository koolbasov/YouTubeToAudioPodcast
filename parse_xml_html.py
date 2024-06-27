from bs4 import BeautifulSoup
import get_xml_html

playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
playlist_xml, playlist_html, playlist_id = get_xml_html.get_html_from_youtube(playlist_url)


soup_html = BeautifulSoup(playlist_html, "html.parser")
feed_title = soup_html.find("meta", property="og:title")
feed_description = soup_html.find("meta", property="og:description")
feed_link = playlist_url


soup_xml = BeautifulSoup(playlist_xml, "xml")
all_items = soup_xml.findAll("entry")
for item in all_items:
    ytb_podcast_id = item.find("yt:videoId").text
    podcast_title = item.find("title")
    ytb_link = item.find("link")["href"]
    ytb_description = item.find("description").text
    ytb_author = item.find("author").text.strip()
    ytb_image = item.find("thumbnail")["url"]

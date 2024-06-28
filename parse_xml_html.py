import datetime as dt
from bs4 import BeautifulSoup

import get_xml_html
import settings

playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
playlist_xml, playlist_html, playlist_id = get_xml_html.get_html_from_youtube(playlist_url)

# сюда мы импортируем функцию из temp_parse_xml когда получим все что нужно

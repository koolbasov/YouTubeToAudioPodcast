from webapp import db, create_app

from webapp.parser_to_db import parse_fields_for_data_base
from webapp.get_xml_html import get_html_from_youtube

playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
playlist_xml, playlist_html, playlist_id = get_html_from_youtube(playlist_url)
playlist_url2 = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMj1oztl-xhl-0A42SwoTvMg"
playlist_xml2, playlist_html2, playlist_id2 = get_html_from_youtube(playlist_url2)

app = create_app()
db.init_app(app)

with app.app_context():
    parse_fields_for_data_base(
        playlist_url, playlist_xml, playlist_html,
        playlist_id, language=2, user_id=1)
    parse_fields_for_data_base(
        playlist_url2, playlist_xml2, playlist_html2,
        playlist_id2, language=2, user_id=1)

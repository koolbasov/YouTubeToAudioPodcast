from flask import Flask

from models import db
from parser_to_db import parse_fields_for_data_base
from get_xml_html import get_html_from_youtube

playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
playlist_xml, playlist_html, playlist_id = get_html_from_youtube(playlist_url)

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
with app.app_context():
    parse_fields_for_data_base(
        playlist_url, playlist_xml, playlist_html,
        playlist_id, language=2, user_id=1)

from webapp import create_app
from webapp.podcast.models import Feed
from webapp.podcast.parser.create_feed import feed_generator
from webapp.podcast.parser.get_xml_html import (
    get_html_from_youtube,
    get_xml_from_youtube,
    get_url_id_from_youtube_link,
)
from webapp.podcast.parser.parser_to_db import parse_fields_for_data_base


app = create_app()

with app.app_context():
    feeds = Feed.query.filter().all()
    if not feeds:
        exit()

    for feed in feeds:
        feed_id = feed.id
        playlist_url = feed.feed_link
        playlist_id = get_url_id_from_youtube_link(playlist_url)
        playlist_xml = get_xml_from_youtube(playlist_url)
        playlist_html = get_html_from_youtube(playlist_url)
        language = feed.lang_id
        user_id = feed.user_id
        if playlist_id and playlist_html and playlist_xml:
            parse_fields_for_data_base(playlist_url, playlist_xml, playlist_html, playlist_id, language, user_id)
            feed_generator(feed_id)

import get_xml_html
import parser
import pprint

playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
playlist_xml, playlist_html, playlist_id = get_xml_html.get_html_from_youtube(playlist_url)

data_for_db = parser.parse_fields_for_data_base(
    playlist_url, playlist_xml, playlist_html, playlist_id)


if __name__ == '__main__':
    pprint.pprint(data_for_db)

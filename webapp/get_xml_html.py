import requests

import config


def check_is_playlist(url):
    is_youtube = "youtu.be" in url or "youtube.com" in url
    is_playlist = "playlist" in url
    if not is_youtube:
        return None
    if not is_playlist:
        return None
    return is_playlist


def get_html_from_youtube(url):
    if not check_is_playlist(url):
        print("Это не youtube плейлист")
        return None
    url_id = url.split("list=")[1]
    playlist_rss = config.RSS_TEMPLATE + url_id
    try:
        response_html = requests.get(url)
        response_xml = requests.get(playlist_rss)
        if response_xml.status_code == 200:
            return response_xml.text, response_html.text, url_id
        elif response_xml.status_code == 404:
            print("Похоже вы пытаетесь загрузить private плейлист")
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Произошла ошибка: {e}")
        return None


if __name__ == "__main__":
    def write_to_file(html, html_id, suffix):
        filename = html_id + suffix
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
            print(f"Файл {f.name} записан")


    playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
    playlist_xml, playlist_html, list_id = get_html_from_youtube(playlist_url)
    if playlist_xml:
        write_to_file(playlist_xml, list_id, ".xml")
        write_to_file(playlist_html, list_id, ".html")

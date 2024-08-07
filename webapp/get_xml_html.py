import requests

from webapp import config


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
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/126.0.0.0 Safari/537.36"
               }
    try:
        response_html = requests.get(url, headers=headers)
        response_xml = requests.get(playlist_rss)
        if response_xml.status_code == 200:
            return response_xml.text, response_html.text, url_id
        elif response_xml.status_code == 404:
            print("Похоже вы пытаетесь загрузить private плейлист")
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"Произошла ошибка: {e}")
        return None

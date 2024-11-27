import requests

from webapp import config


def get_url_id_from_youtube_link(url: str) -> str | None:
    if isinstance(url, str):
        try:
            url_id = url.split("list=")[1]
            return url_id
        except IndexError:
            return None


def is_valid_playlist(url: str) -> bool:
    headers = config.headers
    try:
        response_html = requests.get(url, headers=headers)
        if response_html.status_code == 200:
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False


def get_html_from_youtube(url: str) -> str | None:
    headers = config.headers
    try:
        response_html = requests.get(url, headers=headers)
        if response_html.status_code == 200:
            return response_html.text
        return None
    except requests.exceptions.ConnectionError:
        return None


def get_xml_from_youtube(url: str) -> str | None:
    url_id = get_url_id_from_youtube_link(url)
    if url_id:
        playlist_rss = config.RSS_TEMPLATE + url_id
    else:
        return None
    headers = config.headers
    try:
        response_xml = requests.get(playlist_rss, headers=headers)
        if response_xml.status_code == 200:
            return response_xml.text
        return None
    except requests.exceptions.ConnectionError:
        return None

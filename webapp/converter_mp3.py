import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os

from webapp import config


def download_and_convert_podcast(
        video_url, video_id, feed_title, genre="Podcast"):
    mp3_name = video_id + ".mp3"
    download_path = os.path.join(config.basedir, "static", "podcasts")
    mp3_path = os.path.join(download_path, mp3_name)
    download_options = {
        "quiet": True,
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, video_id),
        'nocheckcertificate': True,
        'addmetadata': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegMetadata'
        }],
    }
    with yt_dlp.YoutubeDL(download_options) as dl:
        if not os.path.exists(mp3_path):
            dl.download([video_url])
            metatag = EasyID3(mp3_path)
            metatag['genre'] = genre
            metatag['album'] = feed_title
            metatag.save()
            audio = MP3(mp3_path)
            duration = int(audio.info.length)
        else:
            audio = MP3(mp3_path)
            duration = int(audio.info.length)
    return duration, mp3_name

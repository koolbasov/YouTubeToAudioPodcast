import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os

from webapp import config


def download_and_convert_podcast(
    video_url: str, video_id: str, feed_title: str, genre: str = "Podcast"
) -> tuple[int, str]:
    mp3_name = video_id + ".mp3"
    mp3_path = os.path.join(config.podcastdir, mp3_name)
    download_options = {
        "quiet": True,
        "format": "bestaudio/best",
        "outtmpl": os.path.join(config.podcastdir, video_id),
        "nocheckcertificate": True,
        "addmetadata": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegMetadata"},
        ],
    }
    with yt_dlp.YoutubeDL(download_options) as dl:
        if not os.path.exists(mp3_path):
            dl.download([video_url])
            metatag = EasyID3(mp3_path)  # type: ignore
            metatag["genre"] = genre
            metatag["album"] = feed_title
            metatag.save()
            audio = MP3(mp3_path)  # type: ignore
            duration = int(audio.info.length)  # type: ignore
        else:
            audio = MP3(mp3_path)  # type: ignore
            duration = int(audio.info.length)  # type: ignore
    return duration, mp3_name

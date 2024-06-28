import yt_dlp
import os

video_id = "SrSl6T1My00"
video_url = "https://www.youtube.com/watch?v=SrSl6T1My00"



# Download data and config

download_options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{video_id}',
        'nocheckcertificate': True,
        'addmetadata':True,
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }, {
            'key': 'FFmpegMetadata'
        }],
}



# https://stackoverflow.com/questions/39885346/youtube-dl-add-metadata-during-audio-conversion
# from mutagen.easyid3 import EasyID3
#
# metatag = EasyID3(pathToMp3File)
# metatag['title'] = "Song Title"
# metatag['artist'] = "Song Artist"
# metatag.RegisterTextKey("track", "TRCK")
# metatag['track'] = 7
# metatag.save()

# Podcast Directory
if not os.path.exists('downloads'):
    os.mkdir('downloads')
else:
    os.chdir('downloads')


# Download Songs
with yt_dlp.YoutubeDL(download_options) as dl:
    dl.download([video_url])


import os

from webapp import config


def delete_podcast_episode(file_name: str) -> None:
    file_path = os.path.join(config.podcastdir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_podcast_episode_image(image_name: str) -> None:
    image_path = os.path.join(config.podcastimagedir, image_name)
    if os.path.exists(image_path):
        os.remove(image_path)


def delete_podcast_feed_image(feed_image: str) -> None:
    feed_image_path = os.path.join(config.feedimagedir, feed_image)
    if os.path.exists(feed_image_path):
        os.remove(feed_image_path)


def delete_podcast_feed_rss(feed_link: str) -> None:
    url_id = feed_link.split("list=")[1]
    rss_filename = f"{url_id}.xml"
    rss_filename_path = os.path.join(config.rssfilesdir, rss_filename)
    if os.path.exists(rss_filename_path):
        os.remove(rss_filename_path)

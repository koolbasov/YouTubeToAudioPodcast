import os

from webapp import config


def delete_podcast_episode(file_name):
    file_path = os.path.join(config.basedir, "static", "podcasts", file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_podcast_episode_image(image_name):
    image_path = os.path.join(config.basedir, "static", "img", image_name)
    if os.path.exists(image_path):
        os.remove(image_path)


def delete_podcast_feed_image(feed_image):
    feed_image_path = os.path.join(config.basedir, "static", "covers", feed_image)
    if os.path.exists(feed_image_path):
        os.remove(feed_image_path)


def delete_podcast_feed_rss(feed_link):
    url_id = feed_link.split("list=")[1]
    rss_filename = f"{url_id}.xml"
    rss_filename_path = os.path.join(config.basedir, "static", "rss", rss_filename)
    if os.path.exists(rss_filename_path):
        os.remove(rss_filename_path)

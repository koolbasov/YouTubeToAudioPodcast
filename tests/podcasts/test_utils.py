from webapp.podcast.utils import (
    delete_podcast_episode,
    delete_podcast_episode_image,
    delete_podcast_feed_image,
    delete_podcast_feed_rss,
)


def test__delete_podcast_episode__file_exists(mp3_file):
    assert delete_podcast_episode(mp3_file) is True


def test__delete_podcast_episode__file_not_exists(file_not_exists):
    assert delete_podcast_episode(file_not_exists) is False


def test__delete_podcast_episode_image__file_exists(image_file):
    assert delete_podcast_episode_image(image_file) is True


def test__delete_podcast_episode_image__file_not_exists(file_not_exists):
    assert delete_podcast_episode_image(file_not_exists) is False


def test__delete_podcast_feed_image__file_exists(feed_image_file):
    assert delete_podcast_feed_image(feed_image_file) is True


def test__delete_podcast_feed_image__file_not_exists(file_not_exists):
    assert delete_podcast_feed_image(file_not_exists) is False


def test__delete_podcast_feed_rss__file_exists(rss_feed_file):
    assert delete_podcast_feed_rss(rss_feed_file) is True


def test__delete_podcast_feed_rss__file_not_exists(valid_play_list):
    assert delete_podcast_feed_rss(valid_play_list) is False

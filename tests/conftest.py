import os
import pytest

from webapp import config


@pytest.fixture()
def valid_play_list():
    return "https://www.youtube.com/playlist?list=PLbr8rVGhPD0WQgO97Ao67Q-QVuSbm_Zpz"


@pytest.fixture()
def private_play_list():
    return "https://www.youtube.com/playlist?list=PLvO-3MXl8QMhfte7dEGGWp2NEA8PfAA-Q"


@pytest.fixture()
def url_id_valid_play_list():
    return "PLbr8rVGhPD0WQgO97Ao67Q-QVuSbm_Zpz"


@pytest.fixture()
def url_id_private_play_list():
    return "PLvO-3MXl8QMhfte7dEGGWp2NEA8PfAA-Q"


@pytest.fixture()
def not_a_play_list():
    return "https://www.youtube.com/watch?v=SVBPkrs9UFg"


@pytest.fixture()
def integer():
    return 123456


@pytest.fixture()
def return_none():
    return None


@pytest.fixture()
def html_text():
    return "<p>Hello Worlds!</p>"


@pytest.fixture()
def xml_text():
    return '<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015"></feed>'


@pytest.fixture()
def mp3_file():
    file_name = "test_file.mp3"
    path_to_file = os.path.join(config.podcastdir, file_name)
    with open(path_to_file, "w") as file_handler:
        file_handler.write("Hello World!")

    yield file_name


@pytest.fixture()
def image_file():
    file_name = "test_file.jpg"
    path_to_file = os.path.join(config.podcastimagedir, file_name)
    with open(path_to_file, "w") as file_handler:
        file_handler.write("Hello World!")

    yield file_name


@pytest.fixture()
def feed_image_file():
    file_name = "test_file.jpg"
    path_to_file = os.path.join(config.feedimagedir, file_name)
    with open(path_to_file, "w") as file_handler:
        file_handler.write("Hello World!")

    yield file_name


@pytest.fixture()
def rss_feed_file(valid_play_list, url_id_valid_play_list):
    feed_link = valid_play_list
    file_name = url_id_valid_play_list + ".xml"
    path_to_file = os.path.join(config.rssfilesdir, file_name)
    with open(path_to_file, "w") as file_handler:
        file_handler.write("Hello World!")

    yield feed_link


@pytest.fixture()
def file_not_exists():
    file_name = "this_file_is_not_exists.txt"
    return file_name

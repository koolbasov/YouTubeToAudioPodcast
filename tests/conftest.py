import pytest


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

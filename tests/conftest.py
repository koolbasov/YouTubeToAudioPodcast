import pytest


@pytest.fixture()
def valid_play_list():
    return "https://www.youtube.com/playlist?list=PLbr8rVGhPD0WQgO97Ao67Q-QVuSbm_Zpz"


@pytest.fixture()
def url_id_right_play_list():
    return "PLbr8rVGhPD0WQgO97Ao67Q-QVuSbm_Zpz"


@pytest.fixture()
def not_a_play_list():
    return "https://www.youtube.com/watch?v=SVBPkrs9UFg"


@pytest.fixture()
def integer():
    return 123456


@pytest.fixture()
def return_none():
    return None

from unittest.mock import patch
import pytest

from webapp.podcast.parser.get_xml_html import get_url_id_from_youtube_link, is_valid_playlist


@pytest.mark.parametrize(
    "url, expected_result",
    [
        ("valid_play_list", "url_id_right_play_list"),
        ("not_a_play_list", "return_none"),
        ("integer", "return_none"),
    ],
)
def test__get_url_id_from_youtube__expected_behavior(url, expected_result, request):
    assert get_url_id_from_youtube_link(request.getfixturevalue(url)) == request.getfixturevalue(expected_result)


def test__get_url_id_from_youtube__two_arguments(valid_play_list, not_a_play_list):
    with pytest.raises(TypeError):
        get_url_id_from_youtube_link(valid_play_list, not_a_play_list)


# def test__is_valid_playlist__valid_playlist(valid_play_list):
#     with (patch("requests.get") as requests_get_mock,):
#         requests_get_mock.status_code.return_value = 200
#         assert is_valid_playlist(valid_play_list) is True

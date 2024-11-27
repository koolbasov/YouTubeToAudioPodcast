import requests
from unittest.mock import patch
import pytest

from webapp.podcast.parser.get_xml_html import (
    get_url_id_from_youtube_link,
    is_valid_playlist,
    get_html_from_youtube,
    get_xml_from_youtube,
)


@pytest.mark.parametrize(
    "url, expected_result",
    [
        ("valid_play_list", "url_id_valid_play_list"),
        ("not_a_play_list", "return_none"),
        ("integer", "return_none"),
    ],
)
def test__get_url_id_from_youtube__expected_behavior(url, expected_result, request):
    assert get_url_id_from_youtube_link(request.getfixturevalue(url)) == request.getfixturevalue(expected_result)


def test__is_valid_playlist__valid_url(valid_play_list):
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = 200
        assert is_valid_playlist(valid_play_list) is True


def test__is_valid_playlist__not_valid_url(private_play_list):
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = 400
        assert is_valid_playlist(private_play_list) is False


def test__is_valid_playlist__connection_error(valid_play_list):
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError) as mock_request:
        mock_request.return_value.side_effect = requests.exceptions.ConnectionError
        assert is_valid_playlist(valid_play_list) is False


def test__get_html_from_youtube__valid_url(valid_play_list, html_text):
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = html_text
        assert get_html_from_youtube(valid_play_list) == html_text


def test__get_html_from_youtube__not_valid_url(private_play_list):
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = 400
        assert get_html_from_youtube(private_play_list) is None


def test__get_html_from_youtube__connection_error(valid_play_list):
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError) as mock_request:
        mock_request.return_value.side_effect = requests.exceptions.ConnectionError
        assert get_html_from_youtube(valid_play_list) is None


def test__get_xml_from_youtube__valid_url(valid_play_list, url_id_valid_play_list, xml_text):
    with (
        patch("webapp.podcast.parser.get_xml_html.get_url_id_from_youtube_link") as mock_get_url_id_from_youtube_link,
        patch("requests.get") as mock_request,
    ):
        mock_get_url_id_from_youtube_link.return_value = url_id_valid_play_list
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = xml_text
        assert get_xml_from_youtube(valid_play_list) == xml_text


def test__get_xml_from_youtube__not_valid_url(private_play_list, url_id_private_play_list):
    with (
        patch("webapp.podcast.parser.get_xml_html.get_url_id_from_youtube_link") as mock_get_url_id_from_youtube_link,
        patch("requests.get") as mock_request,
    ):
        mock_get_url_id_from_youtube_link.return_value = url_id_private_play_list
        mock_request.return_value.status_code = 400
        assert get_xml_from_youtube(private_play_list) is None


def test__get_xml_from_youtube__not_a_playlist(not_a_play_list):
    with (
        patch("webapp.podcast.parser.get_xml_html.get_url_id_from_youtube_link") as mock_get_url_id_from_youtube_link,
    ):
        mock_get_url_id_from_youtube_link.return_value = None
        assert get_xml_from_youtube(not_a_play_list) is None


def test__get_xml_from_youtube__connection_error(valid_play_list, url_id_valid_play_list):
    with (
        patch("webapp.podcast.parser.get_xml_html.get_url_id_from_youtube_link") as mock_get_url_id_from_youtube_link,
        patch("requests.get", side_effect=requests.exceptions.ConnectionError) as mock_request,
    ):
        mock_get_url_id_from_youtube_link.return_value = url_id_valid_play_list
        mock_request.return_value.side_effect = requests.exceptions.ConnectionError
        assert get_xml_from_youtube(valid_play_list) is None

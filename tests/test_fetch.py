from models import Competition, Match
from ingest import get_competitions, get_matches
from unittest.mock import patch, Mock
import pytest


def test_get_competitions_default(mock_competition_valid_response):
    with patch("ingest.fetch.get_request_with_retries") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_competition_valid_response
        mock_get.return_value = mock_response

        result = get_competitions()

    assert len(result) == 2
    codes = [comp.code for comp in result]
    assert "PL" in codes
    assert "ELC" in codes
    assert all(isinstance(comp, Competition) for comp in result)


def test_get_competitions_with_custom_input(mock_competition_valid_response):
    with patch("ingest.fetch.get_request_with_retries") as mock_get:
        mock_return = Mock()
        mock_return.json.return_value = mock_competition_valid_response
        mock_get.return_value = mock_return

        result = get_competitions(["ELC", "PL", "L1"])

    assert len(result) == 3
    codes = [comp.code for comp in result]
    assert "PL" in codes
    assert "ELC" in codes
    assert "L1" in codes
    assert all(isinstance(comp, Competition) for comp in result)


def test_get_competitions_raises_error(mock_invalid_return_value):
    with patch("ingest.fetch.get_request_with_retries") as mock_get:
        mock_return = Mock()
        mock_return.json.return_value = mock_invalid_return_value
        mock_get.return_value = mock_return

        with pytest.raises(KeyError) as excinfo:
            get_competitions()

    assert "competitions" in str(excinfo.value)


def test_get_matches_success_path(mock_match_valid_response, mock_single_competition):
    with patch("ingest.fetch.get_request_with_retries") as mock_get:
        mock_return = Mock()
        mock_return.json.return_value = mock_match_valid_response
        mock_get.return_value = mock_return

        result = get_matches(mock_single_competition, 2024, 1)

    assert len(result) == 2
    assert all(isinstance(match, Match) for match in result)
    matches = [match for match in result]
    assert all([match.matchday == 1 for match in matches])


def get_matches_raises_error(mock_invalid_return_value, mock_single_competition):
    with patch("ingest.fetch.get_request_with_retries") as mock_get:
        mock_return = Mock()
        mock_return.json.return_value = mock_invalid_return_value
        mock_get.return_value = mock_return

        with pytest.raises(KeyError) as excinfo:
            get_matches(mock_single_competition, 2024, 1)

    assert "matches" in str(excinfo.value)

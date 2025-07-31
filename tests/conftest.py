from models import Competition
import pytest


@pytest.fixture
def mock_competition_valid_response():
    return {
        "competitions": [
            {"id": 1, "name": "Premier League", "code": "PL", "type": "LEAGUE"},
            {"id": 2, "name": "Championship", "code": "ELC", "type": "LEAGUE"},
            {"id": 3, "name": "Ligue 1", "code": "L1", "type": "LEAGUE"},
        ]
    }


@pytest.fixture
def mock_single_competition(mock_competition_valid_response):
    id = mock_competition_valid_response["competitions"][0]["id"]
    name = mock_competition_valid_response["competitions"][0]["name"]
    code = mock_competition_valid_response["competitions"][0]["code"]
    type = mock_competition_valid_response["competitions"][0]["type"]

    input_comp = Competition(id=id, name=name, code=code, type=type)
    return input_comp


@pytest.fixture
def mock_match_valid_response():
    return {
        "filters": {"season": 2024, "matchday": "1"},
        "resultSet": {
            "count": 14,
            "first": "2024-08-09",
            "last": "2025-05-09",
            "played": 14,
        },
        "competition": {
            "id": 2016,
            "name": "Championship",
            "code": "ELC",
            "type": "LEAGUE",
            "emblem": "https://crests.football-data.org/ELC.png",
        },
        "matches": [
            {
                "area": {
                    "id": 2072,
                    "name": "England",
                    "code": "ENG",
                    "flag": "https://crests.football-data.org/770.svg",
                },
                "competition": {
                    "id": 2016,
                    "name": "Championship",
                    "code": "ELC",
                    "type": "LEAGUE",
                    "emblem": "https://crests.football-data.org/ELC.png",
                },
                "season": {
                    "id": 2301,
                    "startDate": "2024-08-09",
                    "endDate": "2025-05-24",
                    "currentMatchday": 46,
                    "winner": None,
                },
                "id": 500445,
                "utcDate": "2024-08-09T19:00:00Z",
                "status": "FINISHED",
                "matchday": 1,
                "stage": "REGULAR_SEASON",
                "group": None,
                "lastUpdated": "2025-05-19T09:10:04Z",
                "homeTeam": {
                    "id": 59,
                    "name": "Blackburn Rovers FC",
                    "shortName": "Blackburn",
                    "tla": "BLA",
                    "crest": "https://crests.football-data.org/59.png",
                },
                "awayTeam": {
                    "id": 342,
                    "name": "Derby County FC",
                    "shortName": "Derby County",
                    "tla": "DER",
                    "crest": "https://crests.football-data.org/342.png",
                },
                "score": {
                    "winner": "HOME_TEAM",
                    "duration": "REGULAR",
                    "fullTime": {"home": 4, "away": 2},
                    "halfTime": {"home": 1, "away": 0},
                },
                "odds": {
                    "msg": "Activate Odds-Package in User-Panel to retrieve odds."
                },
                "referees": [
                    {
                        "id": 213800,
                        "name": "Josh Smith",
                        "type": "REFEREE",
                        "nationality": "England",
                    }
                ],
            },
            {
                "area": {
                    "id": 2072,
                    "name": "England",
                    "code": "ENG",
                    "flag": "https://crests.football-data.org/770.svg",
                },
                "competition": {
                    "id": 2016,
                    "name": "Championship",
                    "code": "ELC",
                    "type": "LEAGUE",
                    "emblem": "https://crests.football-data.org/ELC.png",
                },
                "season": {
                    "id": 2301,
                    "startDate": "2024-08-09",
                    "endDate": "2025-05-24",
                    "currentMatchday": 46,
                    "winner": None,
                },
                "id": 500446,
                "utcDate": "2024-08-09T19:00:00Z",
                "status": "FINISHED",
                "matchday": 1,
                "stage": "REGULAR_SEASON",
                "group": None,
                "lastUpdated": "2025-05-19T09:10:04Z",
                "homeTeam": {
                    "id": 1081,
                    "name": "Preston North End FC",
                    "shortName": "Preston NE",
                    "tla": "PNE",
                    "crest": "https://crests.football-data.org/1081.png",
                },
                "awayTeam": {
                    "id": 356,
                    "name": "Sheffield United FC",
                    "shortName": "Sheffield Utd",
                    "tla": "SHE",
                    "crest": "https://crests.football-data.org/356.png",
                },
                "score": {
                    "winner": "AWAY_TEAM",
                    "duration": "REGULAR",
                    "fullTime": {"home": 0, "away": 2},
                    "halfTime": {"home": 0, "away": 1},
                },
                "odds": {
                    "msg": "Activate Odds-Package in User-Panel to retrieve odds."
                },
                "referees": [
                    {
                        "id": 193220,
                        "name": "Bobby Madley",
                        "type": "REFEREE",
                        "nationality": "England",
                    }
                ],
            },
        ],
    }


@pytest.fixture
def mock_invalid_return_value():
    return {"wrong_key": []}

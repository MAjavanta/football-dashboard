from utils.config import config
from models import Competition, Match, Team
import requests

uri = config.API_URI
headers = {"X-Auth-Token": config.FOOTBALL_DATA_API_KEY}


def get_competitions(valid_comps: list[str] | None = None) -> list[Competition]:
    if not valid_comps:
        valid_comps = ["ELC", "PL"]
    route = "/v4/competitions"
    response = requests.get(uri + route, headers=headers)
    all_comps = response.json()["competitions"]
    competitions = [
        Competition(
            id=comp["id"], name=comp["name"], code=comp["code"], type=comp["type"]
        )
        for comp in all_comps
        if comp["code"] in valid_comps
    ]
    return competitions


def get_matches(comp: Competition, season: int, matchday: int) -> list[Match]:
    route = f"/v4/competitions/{comp.id}/matches?season={season}&matchday={matchday}"
    response = requests.get(uri + route, headers=headers)
    all_matches = response.json()["matches"]
    matches = [
        Match(
            id=match["id"],
            utcDatetime=match["utcDate"],
            competition=Competition(
                id=match["competition"]["id"],
                name=match["competition"]["name"],
                code=match["competition"]["code"],
                type=match["competition"]["type"],
            ),
            matchday=match["matchday"],
            homeTeam=Team(
                id=match["homeTeam"]["id"],
                name=match["homeTeam"]["name"],
            ),
            awayTeam=Team(
                id=match["awayTeam"]["id"],
                name=match["awayTeam"]["name"],
            ),
            homeScore=match["score"]["fullTime"]["home"],
            awayScore=match["score"]["fullTime"]["away"],
        )
        for match in all_matches
    ]
    return matches

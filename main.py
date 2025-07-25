import requests
from dotenv import load_dotenv
import os
from models import Competition, Match, Team

load_dotenv()

uri = "https://api.football-data.org"
headers = {"X-Auth-Token": os.getenv("FOOTBALL_DATA_API_KEY")}

comp_list = []
match_list = []


def get_competitions():
    route = "/v4/competitions"
    response = requests.get(uri + route, headers=headers)
    all_comps = response.json()["competitions"]
    valid_comps = ["ELC", "PL"]
    competitions = [
        {
            "id": comp["id"],
            "name": comp["name"],
            "code": comp["code"],
            "type": comp["type"],
        }
        for comp in all_comps
        if comp["code"] in valid_comps
    ]
    for comp_info in competitions:
        comp_list.append(Competition(**comp_info))


def get_matches(comp: Competition, matchday: int = 1):
    route = f"/v4/competitions/{comp.id}/matches?season=2024&matchday={matchday}"
    response = requests.get(uri + route, headers=headers)
    all_matches = response.json()["matches"]
    matches = [
        {
            "id": match["id"],
            "utcDatetime": match["utcDate"],
            "competition": {
                "id": match["competition"]["id"],
                "name": match["competition"]["name"],
                "code": match["competition"]["code"],
                "type": match["competition"]["type"],
            },
            "matchday": match["matchday"],
            "homeTeam": {
                "id": match["homeTeam"]["id"],
                "name": match["homeTeam"]["name"],
            },
            "awayTeam": {
                "id": match["awayTeam"]["id"],
                "name": match["awayTeam"]["name"],
            },
            "homeScore": match["score"]["fullTime"]["home"],
            "awayScore": match["score"]["fullTime"]["away"],
        }
        for match in all_matches
    ]
    for match in matches:
        match["competition"] = Competition(**match["competition"])
        match["homeTeam"] = Team(**match["homeTeam"])
        match["awayTeam"] = Team(**match["awayTeam"])
        match_list.append(Match(**match))


def main():
    get_competitions()
    get_matches(comp_list[0])
    print(match_list)


if __name__ == "__main__":
    main()

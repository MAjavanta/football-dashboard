from utils import config
from models import Competition, Match, Team
import requests
import logging
import time

logger = logging.getLogger(__name__)

uri = config.API_URI
headers = {"X-Auth-Token": config.FOOTBALL_DATA_API_KEY}


def get_request_with_retries(
    route: str, params: dict | None = None, max_retries: int = 3
) -> requests.Response:
    url = uri + route
    logger.debug("Sending request to: %s with params %s", url, params)
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            logger.debug("Success code returned: %s", response.status_code)
            return response
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code and status_code >= 500:
                retries += 1
                logger.warning(
                    "Server error %s, retry %d/%d", status_code, retries, max_retries
                )
                time.sleep(2)
                continue
            else:
                logger.error("HTTP Error %s on %s: %s", status_code, url, e, exc_info=e)
                raise
    raise RuntimeError(
        f"Failed to get successful response from {url} after {retries} retries"
    )


def get_competitions(valid_comps: list[str] | None = None) -> list[Competition]:
    if not valid_comps:
        valid_comps = ["ELC", "PL"]
    logger.debug("Valid comp list: %s", valid_comps)
    route = "/v4/competitions"
    response = get_request_with_retries(route=route)
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
    route = f"/v4/competitions/{comp.id}/matches"
    params = {"season": season, "matchday": matchday}
    response = get_request_with_retries(route=route, params=params)
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

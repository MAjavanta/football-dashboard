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
    """Send a GET HTTP Request to a defined route in the football-data API with a default 3 retry attempts

    Arguments:
        route -- the route that will be added on to the base URL for the GET request
        max_retries -- the number of times the HTTP request will be sent if a Server Error is received

    Keyword Arguments:
        params -- query parameters for the HTTP request that will be added onto the route (default: None)
            NOTE: Should be passed as a dictionary NOT an unpacked dictionary

    Raises:
        RuntimeError: raised when a Server Error has been received max_retries times
        HTTPError: from requests.exceptions, raised when an error code is received from the HTTP request

    Returns:
        requests.Response object
    """
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
    """Returns a list of competitions considered by the football-data API at our current subscription level

    Arguments:
        valid_comps -- An optional list of competition codes (default: None, if None, we consider only PL and ELC)

    Returns:
        A list of Competition objects that are both considered by the football-data API and were passed in as valid
    """
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
    """Get a list of Match details for a given Competition in a given season on a given matchday

    Arguments:
        comp -- a Competition object for the competition whose matches we want to get
        season -- the season of that competition we want to look at (the calendar year it kicked off)
        matchday -- the matchday/matchweek for the matches we want to look at

    Returns:
        a list of Match objects containing details related to the Match, the Competition, and involves Teams
    """
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

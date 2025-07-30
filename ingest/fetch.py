from utils import config
from models import Competition, Match, Team
import requests
import logging
import time

logger = logging.getLogger(__name__)


def get_request_with_retries(
    route: str,
    max_retries: int = 3,
    uri: str = config.API_URI,
    params: dict | None = None,
    headers: dict | None = None,
) -> requests.Response:
    """Send a GET HTTP Request to a defined route in the football-data API with a default 3 retry attempts

    Arguments:
        route -- the route that will be added on to the base URL for the GET request
        max_retries -- the number of times the HTTP request will be sent if a Server Error is received
        uri -- base URL for the GET request (default: config.API_URI from utils)

    Keyword Arguments:
        params -- query parameters for the HTTP request that will be added onto the route (default: None)
            NOTE: Should be passed as a dictionary NOT an unpacked dictionary
        headers -- headers to be sent in GET request in key, value pairs (default: None)
            NOTE: Should typically not be passed as API key is attached in function body if headers is not passed

    Raises:
        RuntimeError: raised when a Server Error has been received max_retries times
        HTTPError: from requests.exceptions, raised when an error code is received from the HTTP request

    Returns:
        requests.Response object
    """
    if not headers:
        headers = {"X-Auth-Token": config.FOOTBALL_DATA_API_KEY}
    url = uri + route
    logger.debug("Sending request to: %s with params %s", url, params)
    retries = 0
    delay_time = config.API_RETRY_DELAY
    while retries < max_retries:
        try:
            response = requests.get(
                url=url, headers=headers, params=params, timeout=config.API_CALL_TIMEOUT
            )
            response.raise_for_status()
            logger.debug("Success code returned: %s", response.status_code)
            return response
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code and status_code >= 500:
                retries += 1
                delay_time *= 2
                logger.warning(
                    "Server error %s, retry %d/%d", status_code, retries, max_retries
                )
                time.sleep(delay_time)
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

    Raises:
        KeyError: raised when response to API call does not contain competitions

    Returns:
        A list of Competition objects that are both considered by the football-data API and were passed in as valid
    """
    if not valid_comps:
        valid_comps = ["ELC", "PL"]
    logger.debug("Getting competitions. Current valid comp list: %s", valid_comps)
    route = "/v4/competitions"
    response = get_request_with_retries(route=route)
    data = response.json()
    if "competitions" not in data:
        raise KeyError(
            f"Key 'competitions' not found in response from GET request to {route}"
        )
    all_comps = data["competitions"]
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
    logger.debug(
        "Getting matches for %s in season beginning %d on matchday %d",
        comp.name,
        season,
        matchday,
    )
    response = get_request_with_retries(route=route, params=params)
    data = response.json()
    if "matches" not in data:
        raise KeyError(
            f"Key 'matches' not found in response from GET request to {route} with params {params}"
        )
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

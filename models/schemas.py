from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class CompType(Enum):
    """
    Enum that lists every possible competition type

    Used for verifying incoming data
    """

    LEAGUE = "LEAGUE"
    CUP = "CUP"


class Competition(BaseModel):
    """Pydantic model of a football competition

    Values:
        id -- unique identifier
        name -- name of competition
        code -- shorthand unique string code representing the competition
        type -- type of competition, a value from the Enum CompType
    """

    id: int
    name: str
    code: str
    type: CompType


class Team(BaseModel):
    """Pydantic model of a football team

    Values:
        int -- unique identifier
        name -- full name of team
    """

    id: int
    name: str


class Match(BaseModel):
    """Pydantic model of a football match

    Values:
        id -- unique identifier
        utcDatetime -- date and time of kick-off, given in UTC time zone
        competition -- Competition object containing details of competition match was played as part of
        matchday -- number representing the matchday/matchweek the match was played in
        homeTeam -- Team object containing details of the home team in the match
        awayTeam -- Team object containing details of the away team in the match
        homeScore -- number of goals scored by the home team
        awayScore -- number of goals scored by the away team
    """

    id: int
    utcDatetime: datetime
    competition: Competition
    matchday: int
    homeTeam: Team
    awayTeam: Team
    homeScore: int
    awayScore: int

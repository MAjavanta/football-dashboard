from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class CompType(Enum):
    LEAGUE = "LEAGUE"
    CUP = "CUP"


class Competition(BaseModel):
    id: int
    name: str
    code: str
    type: CompType


class Team(BaseModel):
    id: int
    name: str


class Match(BaseModel):
    id: int
    utcDatetime: datetime
    competition: Competition
    matchday: int
    homeTeam: Team
    awayTeam: Team
    homeScore: int
    awayScore: int

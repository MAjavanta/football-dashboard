# config.py
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
    API_URI = "https://api.football-data.org"


config = Config()

# config.py
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """Config object containing details used by the rest of the app

    Values:
        FOOTBALL_DATA_API_KEY -- Secret API key used to authorise requests sent to football-data API
        API_URI -- Base URL for requests sent to football-data API
        API_CALL_TIMEOUT -- how long to wait before timing out a request send to football-data API (10 seconds)
        API_RETRY_DELAY -- base value to wait before retrying call to football-data API on server error (1 second)
            NOTE: API_RETRY_DELAY increases exponentially with each retry to avoid thundering herd problem
    """

    FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
    API_URI = "https://api.football-data.org"
    API_CALL_TIMEOUT = 10
    API_RETRY_DELAY = 1


config = Config()

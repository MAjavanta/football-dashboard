import requests
from dotenv import load_dotenv
import os

load_dotenv()

uri = "https://api.football-data.org/v4/matches"
headers = {"X-Auth-Token": os.getenv("FOOTBALL_DATA_API_KEY")}


def get_matches():
    response = requests.get(uri, headers=headers)
    print(response.json())


def main():
    get_matches()


if __name__ == "__main__":
    main()

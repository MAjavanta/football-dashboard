from ingest import get_competitions, get_matches
from utils import LOGGING_CONFIG_DEV
import logging
import logging.config

logging.config.dictConfig(LOGGING_CONFIG_DEV)

comp_list = []
match_list = []


def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting App run")
    comp_list = get_competitions()
    match_list = get_matches(comp_list[1], 2024, 1)
    for match in match_list:
        print(match.model_dump_json())
    logger.info("App run complete")


if __name__ == "__main__":
    main()

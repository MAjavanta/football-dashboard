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
    try:
        comp_list = get_competitions()
    except KeyError as e:
        logger.error("Critical data missing: %s", e)
        raise
    try:
        match_list = get_matches(comp_list[1], 2024, 1)
    except KeyError as e:
        logger.error("Critical missing data: %s", e)
        raise
    for match in match_list:
        print(match.model_dump_json())
    logger.info("App run complete")


if __name__ == "__main__":
    main()

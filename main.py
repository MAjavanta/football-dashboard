from ingest import get_competitions, get_matches

comp_list = []
match_list = []


def main():
    comp_list = get_competitions()
    match_list = get_matches(comp_list[1], 2024, 1)
    for match in match_list:
        print(match.model_dump_json())


if __name__ == "__main__":
    main()

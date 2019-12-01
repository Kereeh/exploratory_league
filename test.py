import cassiopeia as cass
from cassiopeia.core import Summoner, Match, MatchHistory
from cassiopeia import Queue, Patch, Season

cass.set_riot_api_key("RGAPI-a5b0b6e7-6f66-4db3-aaad-af5f59114263")

def print_newest_match(name: str, region: str):
    summoner = Summoner(name = name, region = region)
    match_history = summoner.match_history
    match_history(seasons= {Season.season_9}, queues= {Queue.ranked_solo_fives})

    for match in match_history:
        champion_id = match.participants[summoner.name].champion.id
        match_url = match.participants[summoner.name].match_history_uri

    match = match_history[0]
    print(match.id, match_url, champion_id)

if __name__ == "__main__":
    print_newest_match(name="OG Kayys", region="EUW")


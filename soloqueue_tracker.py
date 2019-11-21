import random
import arrow
import cassiopeia as cass

from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch
from sortedcontainers import SortedList

cass.set_riot_api_key('RGAPI-8a2c970f-d975-405e-b7e8-8ecc4169c588')

def filter_match_history(summoner, patch):
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()

    match_history = MatchHistory(summoner=summoner, queues = {Queue.ranked_solo_fives}, begin_time = patch.start, end_time = end_time)

    return match_history

def collect_matches(summoner_name, region_name):
    
    summoner = Summoner(name = summoner_name, region = region_name)
    patch = Patch.from_str("9.22", region = region_name)

    unpulled_summoner_ids = SortedList([summoner.id])
    pulled_summoner_ids = SortedList()

    unpulled_match_ids = SortedList()
    pulled_match_ids = SortedList()

    while unpulled_summoner_ids:
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region_name)

        matches = filter_match_history(new_summoner, patch)
        unpulled_match_ids.update([match.id for match in matches])

        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.add(new_summoner_id)

        while unpulled_match_ids:
            new_match_id = random.choice(unpulled_match_ids)
            new_match = Match(id=new_match_id, region=region_name)
            
            for participant in new_match.participants:
                if participant.summoner.id not in pulled_summoner_ids and participant.summoner.id not in unpulled_summoner_ids:
                    unpulled_summoner_ids.add(participant.summoner.id)

            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.add(new_match_id)



if __name__ == "__main__":
    collect_matches("Kayys Kayys", "NA")

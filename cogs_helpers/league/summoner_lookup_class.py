from pprint import pprint

import arrow
from cassiopeia import Queue
from collections import defaultdict
from cogs_helpers.league.calculators import win_ratio
from extra_tools import fstat


def get_games_played(item):
    # name, stats = item
    return item[1]["games_played"]


class SummonerLookupAnalysis:
    def __init__(self, summoner):
        self.summoner = summoner
        self.ranked_matches = summoner.match_history(
            queues=[Queue.ranked_solo_fives],
            begin_time=arrow.get(1610085600),
            end_time=arrow.now(),
        )
        self.l20_matches = summoner.match_history(begin_index=0, end_index=20)
        self.ranked_match_count = len(self.ranked_matches)

    def champion_win_rates(self, list_form=True):
        """Returns a list (or dictionary) of champion win-rates in solo queue since this season's start"""
        champ_wrs = {}
        for match in self.l20_matches:
            participant = match.participants[self.summoner]
            champion = participant.champion.name
            match_outcome = participant.team.win
            try:
                champ_wrs[champion]
            except KeyError:
                champ_entry = {champion: defaultdict(int)}
                champ_wrs.update(champ_entry)
            finally:
                if match.is_remake is not True:
                    champ_wrs[champion]["games_played"] += 1
                    if match_outcome is True:
                        champ_wrs[champion]["games_won"] += 1
                    else:
                        champ_wrs[champion]["games_won"] += 0

        champ_wrs = dict(sorted(champ_wrs.items(), key=get_games_played, reverse=True))

        if list_form is False:
            return champ_wrs
        else:
            champs_wrs_list = []
            for champ_name, champ_performance in champ_wrs.items():
                stats = dict(champ_performance)
                games = stats["games_played"]
                wins = stats["games_won"]
                losses = games - wins
                wr = win_ratio(wins, games)
                champs_wrs_list.append(f"**{champ_name}** {wins}W/{losses}L ({wr}%)")

            return champs_wrs_list[0:5]

    def ranked_stats(self):
        """Returns tuple, to be unpacked
        Tuple is returned solo_stats, flex_stats"""
        solo_stats = flex_stats = []
        try:
            solo_queue = self.summoner.league_entries.fives
        except ValueError:
            solo_stats = []
        else:
            solo_stats = [
                f"{solo_queue.tier} {solo_queue.division}",
                f"{solo_queue.wins} W/{solo_queue.losses} L",
                f"{win_ratio(solo_queue.wins, solo_queue.wins + solo_queue.losses)}% WR",
            ]

        try:
            flex_queue = self.summoner.league_entries.flex
        except ValueError:
            flex_stats = []
        else:
            flex_stats = [
                f"{flex_queue.tier} {flex_queue.division}",
                f"{flex_queue.wins} W/{flex_queue.losses} L",
                f"{win_ratio(flex_queue.wins, flex_queue.wins + flex_queue.losses)}% WR",
            ]

        return solo_stats, flex_stats

    def favorite_champs(self):
        m7_champs = self.summoner.champion_masteries.filter(lambda cm: cm.level == 7)
        fav_champs = [fstat(cm.champion.name, f"{cm.points:,d}") for cm in m7_champs]
        return fav_champs[0:5]

    def is_placed_solo(self):
        try:
            self.summoner.league_entries.fives
        except ValueError:
            return False
        else:
            return True

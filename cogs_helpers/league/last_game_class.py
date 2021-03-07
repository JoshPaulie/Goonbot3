from cogs_helpers.league.calculators import kda_ratio, domination_factor, cs_per_min
from extra_tools import fstat


class LastGameAnalysis:
    def __init__(self, summoner):
        """ Class is used to look over the last game played """
        """ QoL Variables """
        self.summoner = summoner
        self.match = self.summoner.match_history()[0]
        self.participant = self.match.participants[summoner]
        self.part_stats = self.participant.stats
        self.timeline = self.participant.timeline
        self.team = self.participant.team
        self.match_outcome = self.part_stats.win
        self.queue = self.match.queue
        self.end_time = self.match.creation.shift(seconds=self.match.duration.seconds)
        self.cs = self.part_stats.total_minions_killed + self.part_stats.neutral_minions_killed

    def kda_stats(self):
        kda_list = [
            fstat(
                f"{self.part_stats.kills}/{self.part_stats.deaths}/{self.part_stats.assists}",
                "KDA",
            ),
            fstat(
                stat=kda_ratio(
                    self.part_stats.kills,
                    self.part_stats.deaths,
                    self.part_stats.assists,
                ),
                desc="KA/D Ratio",
            ),
            fstat(
                stat=domination_factor(
                    self.part_stats.kills,
                    self.part_stats.deaths,
                    self.part_stats.assists,
                ),
                desc="DF",
            ),
        ]
        return kda_list

    def farm_stats(self):
        farm_stats = [fstat(self.cs, "CS"), fstat(cs_per_min(self.cs, self.match.duration.seconds), "CS/Min")]
        return farm_stats

    def carry_stats(self):
        def carry_perc(part_stat, team_stat):
            return f"{round((part_stat / team_stat) * 100)}%"

        # todo make this into a DefaultDict
        team_damage_to_champs = 0
        team_damage_to_obj = 0
        team_kills = 0
        team_deaths = 0
        team_assists = 0
        for participant in self.team.participants:
            team_damage_to_champs += participant.stats.total_damage_dealt_to_champions
            team_damage_to_obj += participant.stats.damage_dealt_to_objectives
            team_kills += participant.stats.kills
            team_deaths += participant.stats.deaths
            team_assists += participant.stats.assists

        damage_to_champs_percent = carry_perc(
            part_stat=self.part_stats.total_damage_dealt_to_champions,
            team_stat=team_damage_to_champs,
        )
        damage_to_obj_percent = carry_perc(
            part_stat=self.part_stats.damage_dealt_to_objectives,
            team_stat=team_damage_to_obj,
        )
        kill_participation = carry_perc(
            part_stat=(self.part_stats.kills + self.part_stats.assists),
            team_stat=team_kills,
        )
        if self.part_stats.deaths != 0:
            death_participation = carry_perc(part_stat=self.part_stats.deaths, team_stat=team_deaths)
        else:
            death_participation = "0%"

        carry_stats_list = [
            fstat(damage_to_champs_percent, "champion damage"),
            fstat(damage_to_obj_percent, "objective damage"),
            fstat(kill_participation, "kill participation"),
            fstat(death_participation, "death participation"),
        ]

        return carry_stats_list

    def multi_kills_stats(self):
        multi_kills_list = [fstat(self.part_stats.largest_killing_spree, "largest spree")]
        if self.part_stats.double_kills > 0:
            multi_kills_list.append(fstat(self.part_stats.double_kills, "double kill(s)!"))
        if self.part_stats.triple_kills > 0:
            multi_kills_list.append(fstat(self.part_stats.triple_kills, "triple kill(s)!"))
        if self.part_stats.quadra_kills > 0:
            multi_kills_list.append(fstat(self.part_stats.quadra_kills, "quadra kill(s)!"))
        if self.part_stats.penta_kills > 0:
            multi_kills_list.append(fstat(self.part_stats.penta_kills, "penta kill(s)!"))
        return multi_kills_list

    def damage_dealt_stats(self):
        damage_list = [
            fstat(self.part_stats.total_damage_dealt_to_champions, "to champs"),
            fstat(self.part_stats.damage_dealt_to_objectives, "to objectives"),
            fstat(self.part_stats.damage_dealt_to_turrets, "to turrets"),
        ]
        return damage_list

    def vision_stats(self):
        vision_list = [
            fstat(self.part_stats.vision_score, "vision score"),
            fstat(self.part_stats.vision_wards_bought_in_game, "pink(s) bought"),
        ]
        return vision_list

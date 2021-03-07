def function_timer(start, end):
    """Returns function execution timer in seconds"""
    diff = end - start
    return f"{diff.seconds}s"


def domination_factor(kills, deaths, assists):
    """Calculate DOMFACT"""
    return (kills * 2) + (deaths * -3) + (assists * 1)


def kda_ratio(kills, deaths, assists):
    """Calculate KD/A and handles perfect games"""
    if deaths > 0:
        return round((kills + assists) / deaths)
    else:
        return "PERF"


def win_ratio(wins, games_played):
    """Calculate w/r and handles perfect w/r"""
    losses = games_played - wins
    if losses > 0:
        return round((wins / (wins + losses)) * 100)
    else:
        return "PERF"


def cs_per_min(cs, game_duration_seconds):
    """Calculate CS/Min"""
    game_duration_minutes = game_duration_seconds / 60
    return round(cs / game_duration_minutes, 2)


victory_defeat_dict = {True: "Victory!", False: "Defeat."}

embed_color_tier = {
    "IRON": 0x565050,
    "BRONZE": 0xA0644D,
    "SILVER": 0x9CA5AA,
    "GOLD": 0xF2C066,
    "DIAMOND": 0x9DB0DB,
    "PLATINUM": 0xA0644D,
    "MASTER": 0xD792C9,
    "GRANDMASTER": 0xF96065,
    "CHALLENGER": 0xFFF5D3,
}

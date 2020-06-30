"""
    This is what runs the actual bot
"""

from config.config_loader import config
from fest.fest_player import FestPlayer
from fest.fest_bot import FestBot

if __name__ == "__main__":
    fest_player_id = config.get("player", "fest_id")
    fest_player_token = config.get("player", "token")
    fest_player = FestPlayer(fest_player_id, fest_player_token)

    print("=" * 20)
    print("Starting the bot...")
    print("Fest Player ID: {}".format(fest_player_id))
    print("Fest Player Token: {}".format(fest_player_token))
    print("=" * 20)

    # Best way of doing this? No, probably not.
    while True:
        FestBot(fest_player).play_all_tourneys()

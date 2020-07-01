import random
from datetime import datetime
import time

from config.config_loader import config
from .fest_tournament import FestTournament
from .constants import TOURNEY_REQUIREMENT_POWERS


class FestBot(object):
    def __init__(self, fest_player):
        self.fest_player = fest_player

    def get_bike_for_requirement(self, requirements):
        player_bikes = self.fest_player.get_player_bikes()
        bike_to_use = None
        descriptor = None

        for bike in player_bikes:
            if "descriptor" in requirements:
                required_bike_id = requirements["descriptor"]["bike_id"]
                if bike["bike_id"] == required_bike_id and not self.fest_player.is_bike_in_use(bike["item_id"]):
                    bike_to_use = bike
                    break
            elif "powers" in requirements:
                required_power = requirements["powers"][0]
                power_character = TOURNEY_REQUIREMENT_POWERS.get(required_power, None)
                if power_character in bike["bike_id"] and not self.fest_player.is_bike_in_use(bike["item_id"]):
                    bike_to_use = bike
                    break
            elif "min_category" in requirements:
                required_category = int(requirements["min_category"])
                bike_category = int(bike["bike_id"][0])
                if (bike_category >= required_category and not self.fest_player.is_bike_in_use(bike["item_id"])):
                    bike_to_use = bike
                    break

        if bike_to_use:
            descriptor = {"type": "bike", "bike_id": bike_to_use["bike_id"]}
        return bike_to_use, descriptor

    def check_for_tasks(self):
        # The method play_all_tourneys is the main method being ran by the bot.
        # However, we have two things we have to do as well:
        #   1. Set times for tourneys that are almost over
        #   2. Claim rewards if this is set as ON in the config.
        # That's what this method will do & this method will be called in play_all_tourneys

        self.set_race_time_for_tourneys()
        
        auto_claim_bot = config.get('bot_configurations', 'auto_claim_tourneys')
        if auto_claim_bot and self.fest_player.has_rewards:
            self.fest_player.claim_rewards()

    def play_all_tourneys(self):
        available_tourneys = self.fest_player.get_available_tournaments()

        # Sort it, so the highest tourneys will be joined first.
        sorted_available_tourneys = sorted(
            available_tourneys, key=lambda i: i["category_id"], reverse=True
        )

        for tourney in sorted_available_tourneys:
            tourney_id = tourney["id"]
            bike, bike_descriptor = self.get_bike_for_requirement(
                tourney["requirements"]
            )
            stamina_fee = tourney["stamina_fee"]

            # check for tasks before joining a new tournament
            self.check_for_tasks()

            if bike is not None and bike_descriptor is not None:
                while stamina_fee > self.fest_player.stamina:
                    self.fest_player.request_stamina_ad()

                    # Sometimes you have zero stamina & it takes long to get stamina for new tournament
                    # So while we request new stamina, we also have to check whether we have tasks to do first.
                    self.check_for_tasks()

                    # The API call allows you to request 1 stamina every give or take 20 second, otherwise you get a invalid response back.
                    time.sleep(20)

                self.fest_player.join_tournament(
                    tourney_id, bike["item_id"], bike_descriptor
                )

    def set_race_time_for_tourneys(self):
        joined_tourneys = self.fest_player.get_joined_tournaments()

        if joined_tourneys:
            try:
                # Play highest tourneys first, those have the best rewards.
                sorted_joined_tourneys = sorted(
                    joined_tourneys, key=lambda i: i["category_id"], reverse=True
                )
            except:
                return "error"

            for tourney in sorted_joined_tourneys:
                fest_tournament = FestTournament(self.fest_player, tourney["id"])
                tourney_end_time = self.iso_time_to_date_time(tourney["expires_at"])
                end_in_sec = self.get_until_in_seconds(tourney_end_time)

                config_end_in_sec = config.get("bot_configurations", "play_before_end_in_seconds")

                if end_in_sec <= config_end_in_sec:
                    for track in tourney["course_info"]["tracks"]:
                        current_best_time = fest_tournament.get_current_best_time_for_track(
                            track["id"]
                        )

                        if current_best_time is not None:
                            # If best time is zero, it means there are no times set & we don't want to submit times <= 0
                            if int(current_best_time) > 0:
                                my_time = int(current_best_time) - random.uniform(0.0001, 0.001)
                            else:
                                my_time = 100

                            fest_tournament.race_track(track["id"], my_time)
                        else:
                            print("You are currently holding #1 positon, so we're not setting new time to prevent attempts wasting.")

    def iso_time_to_date_time(self, tourney_time):
        tourney_time = tourney_time.replace("Z", "")
        return datetime.fromisoformat(tourney_time)

    def get_until_in_seconds(self, tourney_end_time):
        current_time = self.iso_time_to_date_time(datetime.utcnow().isoformat())
        time_until_end = (tourney_end_time - current_time).seconds
        return time_until_end

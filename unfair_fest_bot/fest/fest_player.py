from .fest_client import FestClient
from .constants import *
from config.config_loader import config


class FestPlayer(FestClient):
    def __init__(self, fest_id, token):
        super(FestPlayer, self).__init__(self)
        self.fest_id = fest_id
        self.token = token
        self.base_player_url = BASE_FEST_API_URL + ("players/%s/" % self.fest_id)

    def get_all_player_data(self):
        url = self.base_player_url
        return self.get(url)

    def get_player_slots(self):
        try:
            return self.get_all_player_data()["player"]["slots"]
        except Exception as e:
            print(
                "Something went wrong while trying to retrieve player slots information: {}".format(
                    e
                )
            )
            return []

    def get_player_bikes(self):
        bikes = []
        slots = self.get_player_slots()
        for slot in slots:
            if slot["type"] == "bike":
                bikes.append(slot)
        return bikes

    def get_available_tournaments(self):
        url = self.base_player_url + "tournaments/available"
        json_data = self.get(url)
        return json_data["tournaments"]

    def get_joined_tournaments(self):
        url = self.base_player_url + "tournaments/subscribed"
        json_data = self.get(url)
        return json_data["tournaments"]

    def get_member_rewards(self):
        url = self.base_player_url + "member_rewards/"
        json_data = self.get(url)
        return json_data["member_rewards"]

    def claim_rewards(self):
        member_rewards = self.get_member_rewards()
        url = self.base_player_url + "member_rewards/"

        auto_evolve_bot = config.get("bot_configurations", "auto_evolve")
        spare_turbo_bikes = config.get("bot_configurations", "spare_turbo_bikes")

        for reward in member_rewards:
            reward_id = reward["id"]
            json_data = self.delete(url + reward_id)
            print("Claiming reward: {}".format(reward_id))

            if auto_evolve_bot:
                try:
                    reward_item = json_data["member_rewards"][0]["reward_item"]
                except IndexError:
                    return None
                bike_id = reward_item["bike_id"]

                should_evole = False

                if self.player_has_bike(bike_id):
                    should_evole = True
                    if spare_turbo_bikes and "S" in bike_id:
                        should_evole = False

                if should_evole:
                    self.evolve_after_claim(reward_item["item_id"])

    def join_tournament(self, tournament_id, bike_item_id, bike_descriptor):
        data = {
            "tournament_id": tournament_id,
            "bike_item_id": bike_item_id,
            "bike_descriptor": bike_descriptor,
        }
        url = self.base_player_url + "tournament_memberships"
        print("Joining tournament with ID: {}".format(tournament_id))
        return self.post(url, data)

    def evolve_after_claim(self, part):
        bikes = self.get_player_bikes()
        # 5 star bikes first, 1 star bikes last.
        ordered_bikes = sorted(bikes, key=lambda i: i["bike_id"], reverse=True)
        bike_to_upgrade = None

        # This part can be very slow depending on the amount of bikes in your garage
        # If you don't care about which bike to upgrade, just uncomment the for loop.
        # I'll try to optimize this whenever I have the time.
        for bike in ordered_bikes:
            if not self.is_bike_max_level(bike):
                bike_to_upgrade = bike["item_id"]
                break

        if not bike_to_upgrade or bike_to_upgrade == part:
            bike_to_upgrade = ordered_bikes[0]["item_id"]

        data = {
            "power_up_fusion": {
                "item_ids": [part],
                "tournament_suspensions_accepted": "true",
                "base_bike_id": bike_to_upgrade,
            }
        }
        url = self.base_player_url + "power_up_fusion"
        print("Evolving bike: {}".format(bike_to_upgrade))
        return self.post(url, data)

    def request_stamina_ad(self):
        url = self.base_player_url + "ads"
        print("Requesting stamina so bot can join tournament...")
        return self.post(url)

    def is_bike_in_use(self, bike_item_id):
        joined_tourneys = self.get_joined_tournaments()
        for tourney in joined_tourneys:
            try:
                if tourney["bike_item_id"] == bike_item_id:
                    return True
            except:
                return True
        return False

    def player_has_bike(self, bike_id):
        player_bikes = self.get_player_bikes()
        for bike in player_bikes:
            if bike["bike_id"] == bike_id:
                return True
        return False

    def is_bike_max_level(self, bike):
        items = self.get_items()["items"]
        bike_xp = bike["xp"]

        for item in items:
            if item["descriptor"]["type"] == "bike" and item["descriptor"]["bike_id"] == bike["bike_id"]:
                xp_threshold_len = len(item["metadata"]["xp_level_threshold"])
                xp_level_threshold = item["metadata"]["xp_level_threshold"][xp_threshold_len - 1]

                if bike_xp >= xp_level_threshold:
                    return True
        return False

    @property
    def stamina(self):
        stamina = self.get_all_player_data()["player"]["stamina"]
        return stamina

    @property
    def has_rewards(self):
        unclaimed = self.get_member_rewards()
        return True if len(unclaimed) > 0 else False

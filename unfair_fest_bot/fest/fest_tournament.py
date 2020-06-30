import random

from .fest_client import FestClient


class FestTournament(FestClient):
    def __init__(self, fest_player, tournament_id):
        super(FestTournament, self).__init__(self)
        self.base_url = "https://private-tournaments-api.bikerace.com/tournaments/"
        self.fest_player = fest_player
        self.tournament_id = tournament_id

    def start_track_attempt(self, track_id, random_id):
        url = self.base_url + "{}/started_qualifying_attempts/{}".format(
            self.tournament_id, random_id
        )
        data = {
            "started_qualifying_attempt": {
                "track_id": track_id,
                "player_id": self.fest_player.fest_id,
            }
        }
        return self.put(url, data)

    def finish_track_attempt(self, track_id, my_time, random_id):
        url = self.base_url + "{}/finished_qualifying_attempts/{}".format(
            self.tournament_id, random_id
        )
        data = {
            "finished_qualifying_attempt": {
                "track_id": track_id,
                "player_id": self.fest_player.fest_id,
                "elapsed_time": my_time,
            }
        }
        return self.put(url, data)

    def race_track(self, track_id, my_time):
        random_id = self.get_valid_looking_attempt_id()
        self.start_track_attempt(track_id, random_id)
        self.finish_track_attempt(track_id, my_time, random_id)

    def get_current_best_time_for_track(self, track):
        url = self.base_url + self.tournament_id
        json_data = self.get(url)

        player_best_time = json_data["tournament"]["track_rankings"][track][0]["player_id"]
        if player_best_time == self.fest_player.fest_id:
            return None
        return json_data["tournament"]["track_rankings"][track][0]["best_elapsed_time"]

        # If there's no time, just set it high so we don't generate suspicious times.
        return 100

    def get_valid_looking_attempt_id(self):
        """
			When you race a track, you have to send a id with the request.
			The ID seemed random at first, just length but it's not. Here's a list of working ID's:
			
			"b312c64c-b2f3-4e52-901e-250c24b6f2e1"
			"cf378a46-88f4-4d96-a917-c3a3ab4ffacd"
			"b8070132-2310-4855-8b60-b0b7c7bbf389"
			"4ff3cb35-3e0a-47a3-a84a-ef312dd672ce"
			"000536fc-88df-43dc-a48c-c631aedc25a3"
			"22254f63-a33b-4748-9e35-289f4604ff7b"
			"9c6ccadc-ca4b-4a4b-be4c-8827fcf1afb3"
			"6bba803c-647e-484d-8be6-54ed006d5323"
			"cabff750-b883-4af0-a647-8f28aeb8ae76"
			"0dc8e449-9661-4257-9299-942043f6407a"
			"fc11814f-8ae1-4a51-84dc-637a05c0e255"

			The only thing that seems common for me, is the format and the '4' after the second '-'
			However, when I create something with the format and that 4 it still isn't valid.
			So as of now, this method is not finished and I use the risky thing below (which has never failed for me while testing tho)
		"""
        random_id = "b8070{}32-2{}10-48{}5-8b60-b0b{}c7bbf{}89".format(
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
            random.randint(0, 9),
        )
        return random_id

try:
    import simplejson as json
except ImportError:
    import json
import requests

from .constants import BASE_FEST_API_URL


class FestClient:
    def __init__(self, fest_player):
        self.fest_player = fest_player
        self.base_url = BASE_FEST_API_URL

    @property
    def headers(self):
        return {
            "User-Agent": "moto-pro/8.2.1 (iPhone; iOS 13.2.3; Scale/3.00)",
            "X-Oauth-User": self.fest_player.fest_id,
            "Accept": "application/vnd.topfreegames.com; version=1.6, application/json",
            "Accept-Language": "en-NL;q=1",
            "Token": self.fest_player.token,
            "Accept-Encoding": "gzip, deflate, br",
        }

    # This API call retrieves ALL information about all bikes/parts in Fest.
    def get_items(self):
        url = self.base_url + "items"
        return self.get(url)

    def get(self, url):
        response = None        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTPError: {} - for URL: {}".format(e, url))
        except requests.exceptions.RequestException as e:
            print(
                "Exception while trying to make request: {} - for URL: {}".format(
                    e, url
                )
            )

        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            return response

    def delete(self, url):
        response = None        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTPError: {} - for URL: {}".format(e, url))
        except requests.exceptions.RequestException as e:
            print(
                "Exception while trying to make request: {} - for URL: {}".format(
                    e, url
                )
            )

        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            return response

    def post(self, url, data=None):
        response = None        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTPError: {} - for URL: {}".format(e, url))
        except requests.exceptions.RequestException as e:
            print(
                "Exception while trying to make request: {} - for URL: {}".format(
                    e, url
                )
            )

        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            return response

    def put(self, url, data=None):
        response = None
        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTPError: {} - for URL: {}".format(e, url))
        except requests.exceptions.RequestException as e:
            print(
                "Exception while trying to make request: {} - for URL: {}".format(
                    e, url
                )
            )

        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            return response

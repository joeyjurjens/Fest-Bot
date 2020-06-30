import os
import sys
try:
    import simplejson as json
except ImportError:
    import json


class Config(object):
    def __init__(self):
        self.config_path = os.path.join(sys.path[0], 'config/config.json')

    def open(self):
        try:
            with open(self.config_path) as json_file:
                config_data = json.load(json_file)
        except Exception as e:
            print("Something went wrong while opening your config.json: {}".format(e))
            config_data = None
        return config_data

    def get(self, section, optiom):
        config = self.open()
        if config is not None:
            try:
                return config[section][optiom]
            except Exception as e:
                print("Something went wrong: {}".format(e))
        return None


# Global variable that can be used when importing this file.
config = Config()

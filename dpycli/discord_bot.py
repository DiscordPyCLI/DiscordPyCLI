import os

from .const import yaml


class DiscordBot:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.getcwd()

    def get_bot_config(self):
        yaml_path = os.path.join(self.base_path, "discord.yaml")
        with open(yaml_path) as f:
            return yaml.load(f)

import os

import yaml

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bot_structure.yaml"))

with open(path) as f:
    BOT_STRUCTURE = yaml.load(f, Loader=yaml.FullLoader)
    print(BOT_STRUCTURE)


class BotBuilder:
    def create(self, name, with_cog=None, help_cmd=None):
        print("[INFO:] Creating bot in folder:", name)

        if not with_cog:
            print("[INFO:] No cogs created.")
        else:
            print("[INFO:] Creating cogs:", with_cog)

        if not help_cmd:
            print("No help command generated.")
        elif help_cmd == "template":
            print("[INFO:] Generating Dan6erbond template help command.")
        else:
            print("[INFO:] Generating help command boilerplate.")

    def create_cog(self, bot_file, bot_name, cog):
        if parts := cog.split("-"):
            cog_file = ""
            cog_name = ""

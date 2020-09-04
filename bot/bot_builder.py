import os
from pathlib import Path

import yaml

from .utils import get_cases

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bot_structure.yaml"))

with open(path) as f:
    BOT_STRUCTURE = yaml.load(f, Loader=yaml.FullLoader)


class BotBuilder:
    def __init__(self, bot):
        self.bot = bot
        self.bot_file, self.bot_name = get_cases(bot)
        self.cogs = list()

    def create(self, with_cogs=None, help_cmd=None):
        print("[INFO:] Creating bot in folder:", self.bot_name)

        if not with_cogs:
            print("[INFO:] No cogs created.")
        else:
            print("[INFO:] Creating cogs...")
            for cog in with_cogs:
                self.create_cog(cog)
            if self.cogs:
                self.add_cog_init()

        if not help_cmd:
            print("No help command generated.")
        elif help_cmd == "template":
            print("[INFO:] Generating Dan6erbond template help command.")
        else:
            print("[INFO:] Generating help command boilerplate.")

        self.create_bot_file()

    @property
    def root(self):
        return os.path.abspath(os.path.join(os.getcwd(), self.bot))

    def create_cog(self, cog):
        cog_file, cog_name = get_cases(cog)
        self.cogs.append((cog_file, cog_name))

        cog_folder_path = os.path.join(self.root, "cogs")
        Path(cog_folder_path).mkdir(parents=True, exist_ok=True)

        cog_file_path = os.path.join(cog_folder_path, f"{cog_file}.py")

        with open(cog_file_path, "w+") as f:
            f.write(BOT_STRUCTURE["root"]["cogs"]["{cog_file}.py"].format(
                bot_file=self.bot_file,
                bot_name=self.bot_name,
                cog_name=cog_name))

    def add_cog_init(self):
        cog_folder_path = os.path.join(self.root, "cogs")
        Path(cog_folder_path).mkdir(parents=True, exist_ok=True)

        init_path = os.path.join(cog_folder_path, "__init__.py")

        with open(init_path, "w+") as f:
            f.write("\n".join(f"from .{cog_file} import {cog_name}" for cog_file, cog_name in self.cogs))
            f.write("\n")

    def create_bot_file(self):
        Path(self.root).mkdir(parents=True, exist_ok=True)

        bot_path = os.path.join(self.root, f"{self.bot_file}.py")

        with open(bot_path, "w+") as f:
            cogs_list = ", ".join(f'"cogs.{cog_file}"' for cog_file, _ in self.cogs)
            f.write(
                BOT_STRUCTURE["root"]["{bot_file}.py"].format(
                    bot_name=self.bot_name,
                    cmd_prefix="!",
                    cogs_list=cogs_list,
                    description="Some description."))

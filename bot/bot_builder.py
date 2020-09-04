import os
from pathlib import Path

import inquirer
import yaml

from .utils import get_cases

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bot_structure.yaml"))

with open(path) as f:
    BOT_STRUCTURE = yaml.load(f, Loader=yaml.FullLoader)

VAR_MODES = {"INI File (discord.ini)": "discord.ini",
             "Environment Variables (.env)": ".env",
             "Python File (config.py)": "config.py"}


class BotBuilder:
    def __init__(self, bot):
        self.bot = bot
        self.bot_file, self.bot_name = get_cases(bot)
        self.cogs = list()

    def create(self, with_cogs=None, help_cmd=None):
        print("[INFO:] Creating bot in folder:", self.bot_name)

        questions = [
            inquirer.List("var_mode",
                          message="How would you like to store your client ID and secret?",
                          choices=VAR_MODES.keys(),
                          ),
        ]
        answers = inquirer.prompt(questions)
        var_mode = VAR_MODES[answers["var_mode"]]

        i = input("What command prefix would you like to use for your bot? (default '!') ")
        cmd_prefix = i or "!"

        description = input("Please enter a short bot description: ")
        client_id = input("Please enter your bot's client ID: ")
        token = input("Please enter your bot's token: ")

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

        self.create_var_file(
            var_mode,
            client_id=client_id,
            token=token,
            cmd_prefix=cmd_prefix,
            description=description)
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

    def create_var_file(self, var_mode, **kwargs):
        Path(self.root).mkdir(parents=True, exist_ok=True)

        var_file_path = os.path.join(self.root, var_mode)

        with open(var_file_path, "w+") as f:
            f.write(BOT_STRUCTURE["root"][var_mode].format(bot_name=self.bot_name, **kwargs))

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

import os
from pathlib import Path

import inquirer
from ruamel.yaml import YAML

from .utils import get_cases

yaml = YAML(typ="safe")
yaml.indent(mapping=2, sequence=4, offset=2)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bot_structure.yaml"))
with open(path) as f:
    BOT_STRUCTURE = yaml.load(f)

VAR_MODES = {"[RECOMMENDED:] YAML File (discord.yaml)": "discord.yaml",
             "INI File (discord.ini)": "discord.ini",
             "Environment Variables (.env)": ".env",
             "Python File (config.py)": "config.py"}


class BotBuilder:
    def __init__(self, bot, basic):
        self.bot = bot
        self.basic = basic

        self.bot_file, self.bot_name = get_cases(bot)

        if basic:
            self.bot_name = "bot"

        self.cogs = list()

        self.imports = ["import traceback",
                        "from datetime import datetime",
                        "import discord",
                        "from discord.ext import commands"]

        self.requirements = ["discord.py>=1.4.1"]

    def create(self, with_cogs=None, help_cmd=None):
        print("[INFO:] Creating bot in folder:", self.bot_name)

        questions = [
            inquirer.List("var_mode",
                          message="How would you like to store your bot configuration?",
                          choices=VAR_MODES.keys(),
                          ),
        ]
        answers = inquirer.prompt(questions)
        self.var_mode = VAR_MODES[answers["var_mode"]]

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

        questions = [
            inquirer.List("use_banhammer",
                          message="Would you like to use the Banhammer.py framework in your bot to moderate subreddits?",
                          choices=["Yes", "No"],
                          ),
        ]
        answers = inquirer.prompt(questions)
        use_banhammer = answers["use_banhammer"] == "Yes"

        self.create_var_file(
            client_id=client_id,
            token=token,
            cmd_prefix=cmd_prefix,
            description=description)

        self.create_bot_file(use_banhammer, cmd_prefix, description)

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

    def create_var_file(self, **kwargs):
        Path(self.root).mkdir(parents=True, exist_ok=True)
        var_file_path = os.path.join(self.root, self.var_mode)

        if self.var_mode == "discord.ini":
            self.imports.append("import configparser")
        elif self.var_mode == "config.py":
            self.imports.append("from config import config")

        if self.var_mode == "discord.yaml":
            self.imports.append("from ruamel.yaml import YAML")

            config = {
                self.bot_name: kwargs,
                "cogs": [cog_file for cog_file, _ in self.cogs]
            }

            with open(var_file_path, "w+") as f:
                yaml.dump(config, f)
            return

        with open(var_file_path, "w+") as f:
            f.write(BOT_STRUCTURE["root"]["config"][self.var_mode].format(bot_name=self.bot_name, **kwargs))

    def create_bot_file(self, use_banhammer, cmd_prefix, description):
        Path(self.root).mkdir(parents=True, exist_ok=True)

        bot_path = os.path.join(self.root, f"{self.bot_file}.py")

        with open(bot_path, "w+") as f:
            cogs_list = ", ".join(f'"cogs.{cog_file}"' for cog_file, _ in self.cogs)

            skeleton = BOT_STRUCTURE["root"]["{bot_file}.py"]["skeleton"]

            config = BOT_STRUCTURE["root"]["{bot_file}.py"][f"config-{self.var_mode}"]
            config = config.format(bot_name=self.bot_name, cmd_prefix=cmd_prefix, description=description)

            bot_structure_type = "bot" if not self.basic else "bot-basic"
            bot = BOT_STRUCTURE["root"]["{bot_file}.py"][bot_structure_type]
            bot = bot.format(bot_name=self.bot_name, help_cmd="")

            cogs = "cogs = list()"
            if self.cogs:
                if self.var_mode == "discord.yaml":
                    cogs = 'cogs = config["cogs"]'
                else:
                    cogs = f"cogs = [{cogs_list}]"

            main_structure_type = "main" if not self.basic else "main-basic"
            main = BOT_STRUCTURE["root"]["{bot_file}.py"][main_structure_type]
            main = main.format(bot_name=self.bot_name)

            f.write(skeleton.format(imports="\n".join(self.imports),
                                    config=config,
                                    bot=bot,
                                    banhammer="",
                                    cogs=cogs,
                                    main=main))

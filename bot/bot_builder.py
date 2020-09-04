import os
from pathlib import Path

import inquirer
import requests
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

HELP_CMDS = {"[RECOMMENDED:] Template Help Command": "template",
             "Boilerplate": "boilerplate",
             "No": None}


class BotBuilder:
    def __init__(self, bot, basic):
        self.bot = bot
        self.basic = basic

        self.bot_file, self.bot_name = get_cases(bot)

        if basic:
            self.bot_name = "bot"

        self.cogs = list()

        self.imports = ["import traceback",
                        "import discord",
                        "from discord.ext import commands",
                        "from datetime import datetime"]

        self.requirements = ["discord.py>=1.4.1"]

    def create(self, with_cogs=None):
        print("[INFO:] Creating bot in folder:", self.bot_name)

        question_config = [
            inquirer.List("var_mode",
                          message="How would you like to store your bot configuration?",
                          choices=VAR_MODES.keys(),
                          ),
        ]
        answers = inquirer.prompt(question_config)
        self.var_mode = VAR_MODES[answers["var_mode"]]

        i = input("Choose a command prefix for your bot? (default is: ! ) ")
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

        questions = [
            inquirer.List("help_cmd",
                          message="Would you like to generate a help command?",
                          choices=HELP_CMDS.keys(),
                          ),
        ]
        answers = inquirer.prompt(questions)
        help_cmd = HELP_CMDS[answers["help_cmd"]]

        if not help_cmd:
            print("[INFO:] No help command generated.")
        else:
            self.create_help_cmd(help_cmd)

        question_bh = [
            inquirer.List("use_banhammer",
                          message="Would you like to use the Banhammer.py framework in your bot to moderate subreddits?",
                          choices=["Yes", "No"],
                          ),
        ]
        answers = inquirer.prompt(question_bh)
        use_banhammer = answers["use_banhammer"] == "Yes"

        if use_banhammer:
            if not self.basic:
                self.imports.append("from banhammer import Banhammer")
                self.imports.append("from banhammer.models import EventHandler, RedditItem")
            else:
                self.imports.append("from banhammer import Banhammer")
                self.imports.append("from banhammer.models import RedditItem")

        self.create_var_file(
            client_id=client_id,
            token=token,
            cmd_prefix=cmd_prefix,
            description=description)

        self.create_gitignore()

        self.create_bot_file(use_banhammer, cmd_prefix, description)

    @property
    def root(self):
        return os.path.abspath(os.path.join(os.getcwd(), self.bot))

    def create_help_cmd(self, help_cmd):
        cmds_folder_path = os.path.join(self.root, "cmds")
        Path(cmds_folder_path).mkdir(parents=True, exist_ok=True)

        init_path = os.path.join(cmds_folder_path, "__init__.py")

        with open(init_path, "a+") as f:
            f.write("from .help_cmd import HelpCommand\n")

        help_cmd_file_path = os.path.join(cmds_folder_path, "help_cmd.py")

        if help_cmd == "template":
            with open(help_cmd_file_path, "wb+") as f:
                url = BOT_STRUCTURE["root"]["cmds"]["help_cmd.py"]["template"]
                print("Downloading help_cmd.py...")
                response = requests.get(url)
                total_length = response.headers.get('content-length')
                if total_length is None:
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(25 * dl / total_length)
                        print(f"\r[{'=' * done}{' ' * (25-done)}]", end="\r")
                    print("")
        else:
            with open(help_cmd_file_path, "w+") as f:
                f.write(BOT_STRUCTURE["root"]["cmds"]["help_cmd.py"]["boilerplate"])

    def create_gitignore(self):
        Path(self.root).mkdir(parents=True, exist_ok=True)
        gitignore_file_path = os.path.join(self.root, ".gitignore")

        with open(gitignore_file_path, "wb+") as f:
            url = BOT_STRUCTURE["root"][".gitignore"]
            print("Downloading Python .gitignore template...")
            response = requests.get(url)
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(25 * dl / total_length)
                    print(f"\r[{'=' * done}{' ' * (25-done)}]", end="\r")
                print("")
        with open(gitignore_file_path, "a+") as f:
            f.write(f"\n# Bot config files\n{self.var_mode}\n")

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

        with open(init_path, "a+") as f:
            f.write("\n".join(f"from .{cog_file} import {cog_name}" for cog_file, cog_name in self.cogs))
            f.write("\n")

    def create_var_file(self, **kwargs):
        Path(self.root).mkdir(parents=True, exist_ok=True)
        var_file_path = os.path.join(self.root, self.var_mode)

        if self.var_mode == "discord.ini":
            self.imports.append("import configparser")
        elif self.var_mode == "config.py":
            self.imports.append("from config import config")
        elif self.var_mode == ".env":
            self.imports.append("from dotenv import load_dotenv")

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
            type_sfx = "" if not self.basic else "-basic"

            skeleton = BOT_STRUCTURE["root"]["{bot_file}.py"]["skeleton"]

            config = BOT_STRUCTURE["root"]["{bot_file}.py"][f"config-{self.var_mode}"]
            config = config.format(bot_name=self.bot_name, cmd_prefix=cmd_prefix, description=description)

            bot = BOT_STRUCTURE["root"]["{bot_file}.py"]["bot" + type_sfx]

            bases = "commands.Bot" if not use_banhammer else "commands.Bot, banhammer.Banhammer"

            banhammer_setup = BOT_STRUCTURE["root"]["banhammer"]["setup" + type_sfx]
            banhammer_events = BOT_STRUCTURE["root"]["banhammer"]["events" + type_sfx]
            banhammer_ready = BOT_STRUCTURE["root"]["banhammer"]["ready" + type_sfx]

            def fix_bh_string(string):
                return string.rstrip("\n").replace("\\t", "    ").replace("\\n", "\n")

            bot = bot.format(
                bot_name=self.bot_name,
                help_cmd="",
                bases=bases,
                banhammer_setup=fix_bh_string(banhammer_setup),
                banhammer_events=fix_bh_string(banhammer_events),
                banhammer_ready=fix_bh_string(banhammer_ready))

            cogs = "cogs = list()"
            if self.cogs:
                if self.var_mode == "discord.yaml":
                    cogs = 'cogs = config["cogs"]'
                else:
                    cogs_list = ", ".join(f'"cogs.{cog_file}"' for cog_file, _ in self.cogs)
                    cogs = f"cogs = [{cogs_list}]"

            main = BOT_STRUCTURE["root"]["{bot_file}.py"]["main" + type_sfx]
            main = main.format(bot_name=self.bot_name)

            f.write(skeleton.format(imports="\n".join(self.imports),
                                    config=config,
                                    banhammer="",
                                    bot=bot,
                                    cogs=cogs,
                                    main=main))

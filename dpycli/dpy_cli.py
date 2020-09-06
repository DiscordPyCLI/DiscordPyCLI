import argparse
import os

import click

from .bot_builder import BotBuilder
from .cog_builder import CogBuilder
from .const import yaml
from .discord_bot import DiscordBot
from .utils import get_cases

parser = argparse.ArgumentParser(description="Discord bot CLI scripts.")
parser.add_argument("mode", help="One of 'create', 'add', or 'run'.", choices=["create", "add", "run"])
parser.add_argument("args", help="First additional argument passed to the command.", nargs="*")

"""Bot creation arguments:
@ --cog Adds one or more cogs to the base bot structure.
@ --basic Only instantiates a basic bot, does not create a class.
"""
parser.add_argument(
    "--basic",
    "-b",
    help="Only instantiates a basic bot, does not create a class.",
    nargs="?",
    const=True,
    default=False)
parser.add_argument("--cog", "-c", help="Cogs to include in the bot.", nargs="*")

@click.group()
def main():
    '''
    args = parser.parse_args()

    if args.mode == "create":
        if not args.args:
            print("[ERROR:] The bot's name or a create-mode must be specified.")
            return
        elif args.args[0] == "cog":
            config = DiscordBot().get_bot_config()
            CogBuilder(
                os.getcwd(),
                os.path.basename(config["bot"]["main"]),
                get_cases(config["name"])[1]
            ).add_cog(args.args[1])
        else:
            BotBuilder(args.args[0], args.basic).create(args.cog)
            '''

@main.group()
@click.argument("name", nargs=1, required=False)
def create(name):
    print("Create:", name)

@create.command("*")
@click.argument("name")
def bot(name):
    if name != "cog":
        print("Bot:", name)

@create.command()
@click.argument("name")
def cog(name):
    print("Cog:", name)

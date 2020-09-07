import os

import click

from .bot_builder import BotBuilder
from .cog_builder import CogBuilder
from .const import yaml
from .discord_bot import DiscordBot
from .utils import get_cases


@click.group()
def main():
    pass


"""
Bot creation arguments:
@ name The name of the bot in either camel, snake or kebab case.
@ --cog Adds one or more cogs to the base bot structure.
@ --basic Only instantiates a basic bot, does not create a class.

Cog creation arguments:
@ name The name of the cog in either camel, snake or kebab case.
"""


@main.command()
@click.argument("name", nargs=1, required=True)
@click.option("--basic", "-b", default=False, is_flag=True,
              help="Only instantiates a basic bot, does not create a class.")
@click.option("--cog", "-c", help="Cogs to include in the bot.", multiple=True)
@click.argument("cog-name", nargs=1, required=False)
def create(name, basic, cog, cog_name):
    if name == "cog" and cog_name:
        config = DiscordBot().get_bot_config()
        CogBuilder(
            os.getcwd(),
            os.path.basename(config["bot"]["main"]),
            get_cases(config["name"])[1]
        ).add_cog(cog_name)
    elif name == "cog" and not cog_name:
        print("Argument cog-name is missing!")
    else:
        BotBuilder(name, basic).create(cog)

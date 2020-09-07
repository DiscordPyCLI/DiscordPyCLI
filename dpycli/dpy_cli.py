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


class CreateCommand(click.Group):
    def get_command(self, ctx, cmd_name):
        cmd = click.Group.get_command(self, ctx, cmd_name)
        if cmd:
            return cmd
        else:
            return click.Group.get_command(self, ctx, "bot")


@main.command(cls=CreateCommand)
def create():
    pass


"""
Bot creation arguments:
@ name The name of the bot in either camel, snake or kebab case.
@ --cog Adds one or more cogs to the base bot structure.
@ --basic Only instantiates a basic bot, does not create a class.
"""


@create.command()
@click.option("--basic", "-b", default=False, is_flag=True,
              help="Only instantiates a basic bot, does not create a class.")
@click.option("--cog", "-c", help="Cogs to include in the bot.", multiple=True)
@click.pass_context
def bot(ctx, basic, cog):
    BotBuilder(ctx.info_name, basic).create(cog)


"""
Cog creation arguments:
@ name The name of the cog in either camel, snake or kebab case.
"""


@create.command()
@click.argument("name", nargs=1, required=True)
def cog(name):
    config = DiscordBot().get_bot_config()
    CogBuilder(
        os.getcwd(),
        os.path.basename(config["bot"]["main"]),
        get_cases(config["name"])[1]
    ).add_cog(name)

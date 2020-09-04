import argparse

from .bot_builder import BotBuilder

parser = argparse.ArgumentParser(description="Discord bot CLI scripts.")
parser.add_argument("mode", help="One of 'create', 'add', or 'run'.", choices=["create", "add", "run"])
parser.add_argument("args", help="First additional argument passed to the command.", nargs="*")

"""
Bot creation arguments:
@ --cog Adds one or more cogs to the base bot structure.
@ --basic Only instantiates a basic bot, does not create a class.
"""
parser.add_argument(
    "--basic",
    help="Only instantiates a basic bot, does not create a class.",
    nargs="?",
    const=True,
    default=False)
parser.add_argument("--cog", help="Cogs to include in the bot.", nargs="*", action="extend")


def main():
    args = parser.parse_args()

    if args.mode == "create":
        if not args.args:
            print("[ERROR:] The bot's name must be specified.")
            return
        BotBuilder(args.args[0]).create(args.cog)

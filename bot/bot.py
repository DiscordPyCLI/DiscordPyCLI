import argparse
from .bot_builder import BotBuilder

parser = argparse.ArgumentParser(description="Discord bot CLI scripts.")
parser.add_argument("mode", help="One of 'create', 'add', or 'run'.", choices=["create", "add", "run"])
parser.add_argument("--cog", help="Cogs to include in the bot.", nargs="*", action="extend")
parser.add_argument(
    "--help-cmd",
    help="Whether a help command should be generated.",
    const="boilerplate",
    default=None,
    choices=["template", "boilerplate"],
    nargs="?")
parser.add_argument("args", help="First additional argument passed to the command.", nargs="*")


def main():
    args = parser.parse_args()

    if args.mode == "create":
        if not args.args:
            print("[ERROR:] The bot's name must be specified.")
            return
        BotBuilder(args.args[0]).create(args.cog, args.help_cmd)

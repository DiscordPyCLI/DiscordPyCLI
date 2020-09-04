from setuptools import setup

setup(
    name="discord-bot-builder",
    version="0.0.1",
    entry_points={
        "console_scripts": [
            "bot=bot.bot:main"
        ]
    }
)

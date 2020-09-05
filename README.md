# Discord.py Command Line Tools

A library built by Amelia Cabotte and RaviAnand Mohabir.

DiscordBotBuilder is a set of command line tools inspired by packages such as `npx` and `vue cli` to aid in creating Discord.py bots. The interface enables fast creation of Python projects that follow all the file structure conventions and are typed properly. Goodies such as configuration files, which can be either INI, YAML, Python or `.env` files are supported as well, and a custom `.gitignore` keeps your client information safe.

## Usage

Currently the only working command is `bot create` which supports the following arguments/flags:

 - `name`: The project's name, can be snake, kebab or camel case.
 - `--cog`: Supply cogs that should be generated with the bot.
 - `--basic`: Flag to create a simple instance of a `commands.Bot`, instead of the full class implementation.

Running `bot create my-bot --cog=TestCog` and leaving all the prompts at their default will create the following base folder structure:

```
my-bot /
  cogs /
    __init__.py
    test_cog.py
  .gitignore
  my_bot.py
  requirements.txt
  discord.yaml
```

By default the script will also generate a boilerplate help command by Dan6erbond#2259 with support for pagination and customized outputs. The bot's command prefix, description and support for Banhammer.py can all be customized during the command-run, as you will be prompted to supply additional information.

## Roadmap

 - [ ] `bot add cog`
 - [ ] `bot add cmd`
 - [ ] `bot db create`
 - [ ] `bot db model`

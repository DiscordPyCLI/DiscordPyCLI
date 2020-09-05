import os
from pathlib import Path

from .const import BOT_STRUCTURE, yaml
from .utils import get_cases


class CogBuilder:
    def __init__(self, bot_path, bot_file, bot_name):
        self.bot_path = bot_path
        self.bot_file = bot_file
        self.bot_name = bot_name

    def add_cog(self, cog):
        cog_file, cog_name = get_cases(cog)

        cog_folder_path = os.path.join(self.bot_path, "cogs")
        Path(cog_folder_path).mkdir(parents=True, exist_ok=True)

        cog_file_path = os.path.join(cog_folder_path, f"{cog_file}.py")

        with open(cog_file_path, "w+") as f:
            f.write(BOT_STRUCTURE["root"]["cogs"]["{cog_file}.py"].format(
                bot_file=self.bot_file,
                bot_name=self.bot_name,
                cog_name=cog_name))

        init_path = os.path.join(cog_folder_path, "__init__.py")

        _import = f"from .{cog_file} import {cog_name}"

        import_exists = False
        with open(init_path) as f:
            if _import in f.read():
                import_exists = True

        if not import_exists:
            with open(init_path, "a+") as f:
                f.write(_import)
                f.write("\n")

        return cog_file, cog_name

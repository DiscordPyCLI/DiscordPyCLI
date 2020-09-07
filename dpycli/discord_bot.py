import os
import subprocess
import sys

import requests
from distutils.version import StrictVersion

from .const import yaml


class DiscordBot:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.getcwd()

    @property
    def config(self):
        yaml_path = os.path.join(self.base_path, "discord.yaml")
        with open(yaml_path) as f:
            return yaml.load(f)

    def add_requirement(self, requirement, install=True):
        requirements_file_path = os.path.join(self.base_path, "requirements.txt")

        def split_requirement(req):
            if len(req.split("==")) > 1:
                return req.split("==")
            elif len(req.split(">=")) > 1:
                return req.split(">=")
            elif len(req.split("<=")) > 1:
                return req.split("<=")
            else:
                return req, ""

        name, version = split_requirement(requirement)

        if not version:
            response = requests.get(f"https://pypi.org/pypi/{name}/json")
            versions = list(response.json()["releases"].keys())
            versions.sort(key=StrictVersion)
            pypi_version = versions[-1]

        requirements = list()
        if os.path.exists(requirements_file_path):
            with open(requirements_file_path) as f:
                requirements = [req for req in f.read().splitlines() if split_requirement(req)[0] != name]

        requirements.append(requirement if version else name + ">=" + pypi_version)

        with open(requirements_file_path, "w+") as f:
            f.write("\n".join(requirements) + "\n")

        if install:
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])

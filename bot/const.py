import os

from ruamel.yaml import YAML

yaml = YAML(typ="safe")
yaml.default_flow_style = False
yaml.indent(mapping=2, sequence=4, offset=2)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bot_structure.yaml"))
with open(path) as f:
    BOT_STRUCTURE = yaml.load(f)

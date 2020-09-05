from setuptools import setup
from dpycli import __version__, __tag__

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="DiscordPyCLI",
    version="{}-{}".format(__version__, __tag__) if __tag__ else __version__,
    author="Dan6erbond / Amelia-exe",
    author_email="DiscordPyCLI@gmail.com",
    description="A Discord.py CLI to generate boilerplate code, add dependencies and cogs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "dpy=dpycli.dpy_cli:main"
        ]
    },
    url="https://github.com/DPyCLI/DPyCLI",
    install_requires=requirements,
    keywords="discord bot cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    license="GNU General Public License v3 (GPLv3)",
    python_requires='>=3.6',
)

from setuptools import setup

setup(
    name="discord-bot-builder",
    version="0.0.1",
    author="Dan6erbond",
    author_email="moravrav@gmail.com",
    entry_points={
        "console_scripts": [
            "bot=bot.bot:main"
        ]
    },
    url="https://github.com/Dan6erbond/DiscordBotBuilder",
    install_requires=[
        'inquirer==2.7.0',
        'requests>=2.24.0',
        'ruamel.yaml==0.16.12'
    ],
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

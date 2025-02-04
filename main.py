import os
from sys import argv

from api.main import run_api
from bot.main import run_bot


def main():
    os.system("cls")  # clear screen (works on windows only)
    commands = {"bot": run_bot, "api": run_api}
    command_name = argv[1]
    run_command = commands.get(command_name)
    print(f"🔷 [{command_name}] Running...")
    run_command() if run_command else print("Commands:", ", ".join(commands.keys()))


if __name__ == "__main__":
    main()

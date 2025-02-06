import os
from sys import argv

from api.main import run_api
from bot.main import run_bot


def main():
    apps = {"bot": run_bot, "api": run_api}
    app_names = apps.keys()
    cmd_arg = argv[1] if len(argv) >= 2 else None
    if cmd_arg in app_names:
        os.system(f"cls && title ✈ {cmd_arg}")  # clears & sets title (windows only)
        print(f"📂 {cmd_arg.upper()} app:\n")
        apps.get(cmd_arg)()  # run app
        print("\n❤  Bye!")
    else:
        print(f"'{cmd_arg}' command not available.")
        print("\nCommands:", ", ".join(app_names))


if __name__ == "__main__":
    main()

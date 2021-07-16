"""
Zero-dependency bootstrap script

.. todo::

    lift to `packutil`
"""
import argparse
import subprocess


def load_options(yes, no, default):
    yes_choice = "[Y/n]"
    no_choice = "[y/N]"

    def question(input_text, default_yes):
        if not any([yes, no, default]):
            choice = yes_choice if default_yes else no_choice
            answer = input(f"Do you want to install with pipx? {choice} ")
        else:
            if yes:
                answer = "y"
            elif no:
                answer = "n"
            answer = "y" if default_yes else "n"
        return answer

    return question


def parse_args():
    parser = argparse.ArgumentParser()

    silence = parser.add_mutually_exclusive_group()
    silence.add_argument(
        "-y", "--yes", action="store_true", help="yes to every questions"
    )
    silence.add_argument(
        "-n", "--no", action="store_true", help="no to every questions"
    )
    silence.add_argument(
        "--default", action="store_true", help="default to every questions"
    )

    parser.add_argument(
        "--user",
        action="store_true",
        help="install user wide (only relevant for pip installation)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    question = load_options(args.yes, args.no, args.default)

    answer = question("Do you want to install with pipx? [y/N] ", False)
    if answer.lower() in ["y", "yes"]:
        print("installing with pipx...")
        subprocess.call("pipx install poetry".split())
        subprocess.call("pipx inject poetry poetry-dynamic-versioning".split())
        subprocess.call("pipx install pre-commit".split())
    else:
        print("installing with pip...")
        user = " --user" if args.user else ""
        subprocess.call(f"pip install{user} poetry".split())
        subprocess.call(f"pip install{user} poetry-dynamic-versioning".split())
        subprocess.call(f"pip install{user} pre-commit".split())
    subprocess.call("poetry install".split())

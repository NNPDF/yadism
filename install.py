"""
Zero-dependency bootstrap script
"""
import argparse
import pathlib
import shutil
import subprocess

here = pathlib.Path(".").parent.absolute()


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


def load_options(yes, no, default):
    yes_choice = "[Y/n]"
    no_choice = "[y/N]"

    def question(input_text, default_yes):
        if not any([yes, no, default]):
            choice = yes_choice if default_yes else no_choice
            answer = input(f"{input_text} {choice} ")
        else:
            if yes:
                answer = "y"
            elif no:
                answer = "n"
            else:
                answer = "y" if default_yes else "n"
        return answer

    return question


def repo_management(pipx, user):
    if pipx:
        print("installing management dependecies with pipx...")
        subprocess.call("pipx install poetry".split())
        subprocess.call("pipx inject poetry poetry-dynamic-versioning".split())
        subprocess.call("pipx install pre-commit".split())
    else:
        print("installing management dependecies with pip...")
        subprocess.call(f"pip install{user} poetry".split())
        subprocess.call(f"pip install{user} poetry-dynamic-versioning".split())
        subprocess.call(f"pip install{user} pre-commit".split())


if __name__ == "__main__":
    args = parse_args()

    question = load_options(args.yes, args.no, args.default)

    if shutil.which("pipx") is not None:
        pipx_answer = question("Do you want to install with pipx?", False)
    else:
        pipx_answer = "no"

    pipx = pipx_answer.lower() in ["y", "yes"]
    user = " --user" if args.user else ""
    repo_management(pipx, user)

    subprocess.call("poetry install".split())

"""
Zero-dependency bootstrap script

.. todo::

    lift to `packutil`
"""
import argparse
import importlib
import pathlib
import re
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

    parser.add_argument(
        "--non-pip",
        choices=["no", "only"],
        help="control installation of non-pip dependecies",
    )

    parser.add_argument(
        "--clean", action="store_true", help="just clean the generated assets"
    )

    return parser.parse_args()


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
            else:
                answer = "y" if default_yes else "n"
        return answer

    return question


def format_long_string(string, length=80, first_shift=0):
    string = re.sub("\n *", " ", string).strip()

    lines = []
    cur_length = length - first_shift
    while string:
        if len(string) < cur_length:
            lines.append(string)
            string = ""
        else:
            try:
                ws_pos = string[:cur_length].rindex(" ")
            except ValueError:
                try:
                    ws_pos = string.index(" ")
                except ValueError:
                    ws_pos = len(string)
            lines.append(string[:ws_pos])
            string = string[ws_pos + 1 :]
        cur_length = length

    return "\n".join(lines)


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


def trim_pkg(path):
    return path.stem.split(".")[0] + path.suffix


def nonpip_dependency(pkg, dir_):
    try:
        pkg = importlib.import_module(pkg)
        path = pathlib.Path(pkg.__file__)
        shutil.copy2(path, dir_ / trim_pkg(path))
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            format_long_string(
                f"""Package {pkg} not found, please compile and make it
                available for your current python""",
                first_shift=len("ModuleNotFoundError: "),
            )
        )


def clean(nonpip):
    for pkg in nonpip:
        try:
            pkg = importlib.import_module(pkg)
            (here / "benchmarks" / trim_pkg(pathlib.Path(pkg.__file__))).unlink(
                missing_ok=True
            )
        except ModuleNotFoundError:
            pass


nonpip = ["lhapdf", "apfel", "_apfel"]

if __name__ == "__main__":
    args = parse_args()

    if args.clean:
        clean(nonpip)
        quit()

    question = load_options(args.yes, args.no, args.default)

    if args.non_pip != "only":
        pipx_answer = question("Do you want to install with pipx? [y/N] ", False)

        pipx = pipx_answer.lower() in ["y", "yes"]
        user = " --user" if args.user else ""
        repo_management(pipx, user)

    if args.non_pip != "no":
        print("installing nonpip dependecies...")
        for pkg in nonpip:
            nonpip_dependency(pkg, here / "benchmarks")
        # install everything only with nonpip dependecies, otherwise will fail
        subprocess.call("poetry install".split())

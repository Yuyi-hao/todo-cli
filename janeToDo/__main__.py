"""
Entry point script for Jane To-Do.
Path: janeToDo/__main__.py
"""

from janeToDo import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
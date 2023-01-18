"""
This module provides Jane To-Do database functionality.
Path: janeToDo/database.py
"""

import json
import configparser
from pathlib import Path
from typing import Any, Dict, NamedTuple, List
from janeToDo import (
    DB_WRITE_ERROR,
    SUCCESS,
    DB_READ_ERROR,
    JSON_ERROR
)


DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    f"{Path.home().stem}_todo.json"
)


def get_database_path(config_file: Path) -> Path:
    """
    Return the current path to the to-do database.
    :param config_file:
    :return:
    """
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """
    Create the to-do database
    :param db_path:
    :return:
    """
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        """
        To read from json data
        :return:
        """
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # catching for wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # file IO problem
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        """
        To write in database
        :param todo_list:
        :return:
        """
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)

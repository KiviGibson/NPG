import sqlite3 as sqlite
from enum import Enum
from typing import Type
from dataclasses import dataclass


@dataclass(frozen=True)
class PressureData:
    """DataClass storing info about pressure"""

    _id: int
    date: int
    value: float
    desc: str


class Database:
    """Class that holds Database Api logic"""

    def __init__(self, db: str) -> None:
        self._db = sqlite.connect(db)
        cursor = self._db.cursor()
        cursor.execute("SELECT name FROM sqlite_master;")
        tables = cursor.fetchall()
        if not ("pressure",) in tables:
            cursor.execute(
                """
                CREATE TABLE pressure(
                    id INTEGER PRIMARY KEY, 
                    user_id INTEGER, 
                    date INTEGER, 
                    value REAL, 
                    desc TEXT, 
                    FOREIGN KEY(user_id) REFERENCES user(id));
                """
            )
        if not ("user",) in tables:
            cursor.execute(
                """
                CREATE TABLE user(
                    id INTEGER PRIMARY KEY, 
                    login TEXT, 
                    password TEXT);
                """
            )
        self._db.commit()
        print("Database connected")

    def close(self) -> None:
        self._db.close()
        print("Database disconnected")


if __name__ == "__main__":
    d = Database("test.db")
    d.close()

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
        if "pressure" in cursor.fetchall():
            print("Database connected")
            return
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
        cursor.execute(
            """
            CREATE TABLE user(
                id INTEGER PRIMARY KEY, 
                login TEXT, 
                password TEXT);
            """
        )
        self._db.commit()
        print("Database created")

    def __exit__(self) -> None:
        self._db.close()


if __name__ == "__main__":
    d = Database("test.db")

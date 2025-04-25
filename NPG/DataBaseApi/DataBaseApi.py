import sqlite3 as sqlite
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

    def getUser(self, login: str, password: str) -> int:
        cursor = self._db.cursor()
        cursor.execute(
            """
            SELECT id FROM user 
            WHERE login = ? AND password = ?;
            """,
            [login, password],
        )
        data = cursor.fetchall()
        if len(data) != 1:
            return -1
        return data[0][0]

    def createUser(self, login: str, password: str) -> None | int:
        cursor = self._db.cursor()
        cursor.execute(
            """
            SELECT id FROM user 
            WHERE login = ?;
            """,
            [login],
        )
        if len(cursor.fetchall()) > 0:
            return -1
        cursor.execute(
            """
            INSERT INTO user(login, password) VALUES(?,?);
            """,
            [login, password],
        )
        self._db.commit()

    def close(self) -> None:
        self._db.close()
        print("Database disconnected")


if __name__ == "__main__":
    d = Database("test.db")
    d.close()

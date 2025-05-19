import sqlite3 as sqlite
from typing import Type
from dataclasses import dataclass


@dataclass(frozen=True)
class PressureData:
    """DataClass storing info about pressure"""

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
            return -404
        return data[0][0]  # [(val,)] -> val

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
            return -400
        cursor.execute(
            """
            INSERT INTO user(login, password) VALUES(?,?);
            """,
            [login, password],
        )
        self._db.commit()
        return None

    def getData(
        self,
        id: int,
        date: tuple[int, int] | None = None,
        value: tuple[float, float] | None = None,
    ) -> list[PressureData]:
        res: list[PressureData] = []
        cursor = self._db.cursor()
        query: str = "SELECT date, value, desc FROM pressure WHERE user_id = ? "
        params: list = [id]
        if date is not None:
            query += " AND (date BETWEEN ? AND ?) "
            params.append(date[0])
            params.append(date[1])
        if value is not None:
            query += " AND (value BETWEEN ? AND ?) "
            params.append(value[0])
            params.append(value[1])
        cursor.execute(query + ";", params)
        for datum in cursor.fetchall():
            res.append(PressureData(datum[0], datum[1], datum[2]))
        return res

    def addData(self, id: int, datum: PressureData) -> None:
        cursor = self._db.cursor()
        query = "INSERT INTO pressure(user_id, date, value, desc) VALUES(?, ?, ?, ?);"
        params = [id, datum.date, datum.value, datum.desc]
        cursor.execute(query, params)
        self._db.commit()

    def close(self) -> None:
        self._db.close()
        print("Database disconnected")


if __name__ == "__main__":
    d = Database(":memory:")
    d.close()

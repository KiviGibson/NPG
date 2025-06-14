import sqlite3 as sqlite
from dataclasses import dataclass


@dataclass(frozen=True)
class PressureData:
    """DataClass storing info about pressure"""

    date: int
    value: list[float]
    desc: str


class Database:
    """Class that holds Database Api logic"""

    def __init__(self, db: str) -> None:
        self._db = sqlite.connect(db, check_same_thread=False)
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
                    sys REAL,
                    dys REAL,
                    pulse REAL, 
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

    def getUser(self, login: str) -> tuple | int:
        cursor = self._db.cursor()
        cursor.execute(
            """
            SELECT id, password FROM user 
            WHERE login = ?;
            """,
            [login],
        )
        data = cursor.fetchall()
        if len(data) != 1:
            return -404
        return data[0]  # [(id, password)] -> (id, password)

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
        self, id: int, filters: dict[str, tuple[float, float]] = {}
    ) -> list[PressureData]:
        """
        Dopuszczalne filtry: date, sys, dys, pulse i zawsze 2 wartości lub MAX
        """
        keys = ["date", "sys", "dys", "pulse"]
        res: list[PressureData] = []
        cursor = self._db.cursor()
        query: str = (
            "SELECT date, sys, dys, pulse, desc FROM pressure WHERE user_id = ? "
        )
        params: list = [id]
        for key, value in filters.items():
            if key not in keys:
                continue
            query += f" AND ({key} BETWEEN ? AND ?) "
            params.append(value[0])
            params.append(value[1])
        cursor.execute(query + ";", params)
        for datum in cursor.fetchall():
            res.append(PressureData(datum[0], datum[1:4], datum[4]))
        return res

    def addData(self, id: int, datum: PressureData) -> None:
        cursor = self._db.cursor()
        query = "INSERT INTO pressure(user_id, date, sys, dys, pulse, desc) VALUES(?, ?, ?, ?, ?, ?);"
        params = [id, datum.date, *datum.value, datum.desc]
        cursor.execute(query, params)
        self._db.commit()

    def close(self) -> None:
        self._db.close()
        print("Database disconnected")


if __name__ == "__main__":
    d = Database(":memory:")
    d.close()

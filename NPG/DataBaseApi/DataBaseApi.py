import sqlite3 as sqlite
from enum import Enum
from typing import Type
from dataclasses import dataclass


class Query:
    def __init__(self) -> None:
        self._query: str = ""
        print("Query Created")

    def getQuery(self) -> str:
        print(self._query+";")
        return self._query + ";"


@dataclass(frozen = True)
class PressureData:
    """DataClass storing info about pressure"""
    _id: int
    date: int
    value: float
    desc: str


class DataBase:
    """ Class that holds Database Api logic"""
    def __init__(self, db: str) -> None:
        self._db = sqlite.connect(db)
        cursor = self._db.cursor()
        cursor.execute("SELECT name FROM sqlite_master;")
        if "pressure" in cursor.fetchall():
            print("Database connected")
            return
        cursor.execute("CREATE TABLE pressure(id INTEGER PRIMARY KEY, date INTEGER, value REAL, desc TEXT);")
        self._db.commit()
        print("Database created")
    

    def execute(self, query: Query) -> list[PressureData]:
        queryString = query.getQuery()
        if query.getType() == QueryType.undefined:
            raise Exception("Can't Execute undefined query")
        try:
            cursor = self._db.cursor()
            cursor.execute(queryString)
            print("Operation Successful")
            if query.getType() == QueryType.insert: 
                self._db.commit()
                return []
            return [PressureData(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
        except sqlite.OperationalError:
            print("Operation was not Successful!")
            return []

    def __exit__(self) -> None:
        self._db.close()


class QueryType(Enum):
    undefined = 0
    select = 1
    insert  = 2


class PressureQuery(Query):
    """Builder for SQLITE Query"""
    def __init__(self):
        super().__init__()
        self._type: QueryType = QueryType.undefined
        self._param: bool = False

    def select(self) -> Query:
        """Swaps to SELECT Query"""
        self._query = "SELECT * FROM pressure"
        self._type = QueryType.select
        self._param = False
        return self
    
    def insert(self) -> Query:
        """Swaps to INESRT Query"""
        self._query = "INSERT INTO pressure(date, value, desc) VALUES"
        self._type = QueryType.insert
        self._param = False
        return self
    
    def addDateRange(self, f: int, t: int = 0) -> Query:
        """Adds date range for SELECT query"""
        if self._type != QueryType.select: return self
        if not self._param:
            self._query += f" WHERE (date BETWEEN {f} AND {f+t})"
            self._param = True
        else:
            self._query += f" AND (date BETWEEN {f} AND {f+t})"
        return self

    def addPressureRange(self, f: float, t: float = 0) -> Query:
        """Adds pressure value range for SELECT query"""
        if self._type != QueryType.select: return self
        if not self._param:
            self._query += f" WHERE (value BETWEEN {f} AND {f+t})"
            self._param = True
        else:
            self._query += f" AND (value BETWEEN {f} AND {f+t})"
        return self
    
    def addLimit(self, amount: int, first: int = 0) -> Query:
        """Adds max item LIMIT for SELECT query"""
        if self._type != QueryType.select: return self
        self._query += f" LIMIT {first}, {amount}"
        return self

    def addValue(self, datum: PressureData) -> Query:
        """Adds new item for INSERT query"""
        if self._type != QueryType.insert: return self
        if self._param:
            self._query += f", ({datum.date}, {datum.value}, \"{datum.desc}\")"
        else:
            self._query += f" ({datum.date}, {datum.value}, \"{datum.desc}\")"
            self._param = True
        return self

    def getType(self) -> QueryType:
        """Returns type of query"""
        return self._type


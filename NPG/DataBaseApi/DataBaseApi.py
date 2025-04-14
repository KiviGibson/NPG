import sqlite3 as sqlite 
from dataclasses import dataclass


class DataBase:
    """ Class that holds Database Api logic"""
    def __init__(self, db: str) -> None:
        self._db = sqlite.connect(db)
        cursor = self._db.cursor()
        cursor.execute("SELECT name FROM sqlite_master;")
        if pressure in crs.fetchall():
            print("Database connected")
            return
        cursor.execute("CREATE TABLE pressure(id INTEGER PRIMARY KEY, date INTEGER, value REAL, desc TEXT);")
        self._db.commit()
        print("Database created")
    

    def execute(query: Query) -> List:
        queryString = query.getQuery()
        if query.getType == QueryType.undefined:
            raise Exception("Can't Execute undefined query")
        try:
            cursor = self._db.cursor()
            cursor.execute(queryString)
            if query.getType() == QueryType.insert: 
                cursor.commit()
                return []
            return [PressuereData(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()] 
        except sqlite.OperationalError:
            print("Operation was not Successful!")
            return []

    def __exit__(self) -> None:
        self._db.close()


@dataclass(freeze = True)
class PressuereData:
    """DataClass storing info about pressure"""
    _id: int
    date: int
    value: float
    desc: str


class Query:
    def __init__(self) -> None:
        self._query: str = ""
        print("Query Created")

    def getQuery(self) -> str:
        return self._query + ";"

class QueryType(Enum):
    undefined -> 0
    select -> 1
    insert -> 2

class PressureQuery(Query):
    """Builder for SQLITE Query"""
    def __init__(self):
        super().__init__(self)
        self._type: QueryType = QueryType.undefined
        self._param: bool = False

    def select() -> PressureQuery:
        """Swaps to SELECT Query"""
        self.query = "SELECT * FROM pressure"
        self._type = QueryType.select
        self._param = False
        return self
    
    def insert() -> PressureQuery:
        """Swaps to INESRT Query"""
        self.query = "INSERT INTO pressure(date, value, desc) VALUES"
        self._type = QueryType.insert
        self._param = False
        return self
    
    def addDateRange(self, from: int, to: int = from) -> PressureQuery:
        """Adds date range for SELECT query"""
        if self._type != QueryType.select: return self
        if not self._param:
            self._query += f" WHERE date between ({from}, {to})"
            self._param = True
        else:
            self._query += f" AND date BETWEEN ({from}, {to})"
        return self

    def addPressureRange(from: float, to: float = from) -> PressureQuery:
        """Adds pressure value range for SELECT query"""
        if self._type != QueryType.select: return self
        if not self._param:
            self._query += f" WHERE date BETWEEN ({from}, {to})"
            self._param = True
        else:
            self._query += f" AND date BETWEEN ({from}, {to})"
        return self
    
    def addLimit(self, amount: int, first: int = 0) -> PressureQuery:
        """Adds max item LIMIT for SELECT query"""
        if self._type != QueryType.select: return self
        self._query += f" LIMIT {amount}, {first}"
        return self

    def addValue(datum: PressuereData) -> None:
        """Adds new item for INSERT query"""
        if self._type != QueryType.insert: return self
        if self._param:
            self._query += f", ({datum.date}, {datum.value}, \"{datym.desc}\")"
        else:
            self._query += f" ({datum.date}, {datum.value}, \"{datym.desc}\")"
            self._param = True
        return self

    def getType() -> QueryType:
        return self._type


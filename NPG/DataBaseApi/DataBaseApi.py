import sqlite3 as sqlite 
from dataclasses import dataclass
class DataBase:
    """ Class that holds Database Api logic"""
    def __init__(self):
        pass


@dataclass
class PressuereData:
    """DataClass storing info about pressure"""
    date: int
    value: float
    desc: str

class PressureQuery:
    def __init__(self):
        query: str = "SELECT * FROM pressure"

    def addDateRange(self, f: int, t: int = f) -> PressureQuery:
        if !(query.find("WHERE")):
            query += f" WHERE date between ({f}, {t})"
        else:
            query += f" AND date BETWEEN ({f}, {t})"
        return self

    def addPressureRange(f: float, t: float = f) -> PressureQuery:
        if query.find("WHERE"):
            query += f" WHERE date BETWEEN ({f}, {t})"
        else:
            query += f" AND date BETWEEN ({f}, {t})"
        return self
    
    def addLimit(self, amount: int, first: int = 0) - > PressureQuery:
        query += f" LIMIT {amount}, {first}"
        return self

    def build() -> str:
        return query + ";"


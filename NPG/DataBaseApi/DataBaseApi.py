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


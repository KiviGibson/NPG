from jwt import encode, decode
from ..DataBaseApi import Database


class Auth:
    def __init__(self, db: Database) -> None:
        self._db = db

    def checkCredentials(self, jwt: str) -> int:
        return 0

    def login(self, login: str, password: str) -> str | int:
        id = self._db.getUser(login, password)
        if id == -1:
            return ""
        return encode(
            {"login": login, "password": password}, "passphrase", algorithm="HS256"
        )

    def register(self, login: str, password: str) -> str | int:
        return ""

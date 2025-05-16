from jwt import encode, decode
from .DataBaseApi import Database


class Auth:
    def __init__(self, db: Database) -> None:
        self._db = db

    def checkCredentials(self, jwt: str | None) -> int:
        if jwt is None:
            return -1
        login, password = decode(jwt, "passphrase", algorithms=["HS256"])
        return self._db.getUser(login, password)

    def login(self, login: str, password: str) -> str | int:
        id = self._db.getUser(login, password)
        if id == -1:
            return -1
        return encode(
            {"login": login, "password": password}, "passphrase", algorithm="HS256"
        )

    def register(self, login: str, password: str) -> str | int:
        if self._db.createUser(login, password) == -1:
            return -1
        return self.login(login, password)

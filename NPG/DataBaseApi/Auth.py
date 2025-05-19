from jwt import encode, decode
from .DatabaseApi import Database


class Auth:
    def __init__(self, db: Database) -> None:
        self._db = db

    def check_credentials(self, token: str | None) -> int:
        if token is None:
            print("No token")
            return -418
        data = decode(token, "passphrase", algorithms=["HS256"])
        return self._db.getUser(data["login"], data["password"])

    def login(self, login: str, password: str) -> str | int:
        id = self._db.getUser(login, password)
        if id == -404:
            return -404
        return encode(
            {"login": login, "password": password}, "passphrase", algorithm="HS256"
        )

    def register(self, login: str, password: str) -> str | int:
        id = self._db.createUser(login, password)
        if id == -400:
            return -400
        return self.login(login, password)


if __name__ == "__main__":
    d = Database(":memory:")
    a = Auth(d)
    jwt = a.register("Kivi", "Gibson")
    if type(jwt) is str:
        print(a.check_credentials(jwt))
    print("Womp Womp")

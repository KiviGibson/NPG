from jwt import encode, decode
from DatabaseApi import Database


class Auth:
    def __init__(self, db: Database) -> None:
        self._db = db

    def checkCredentials(self, jwt: str) -> int:
        data = decode(jwt, "passphrase", algorithms=["HS256"])
        return self._db.getUser(data["login"], data["password"])

    def login(self, login: str, password: str) -> str | int:
        id = self._db.getUser(login, password)
        if id == -1:
            return -1
        return encode(
            {"login": login, "password": password}, "passphrase", algorithm="HS256"
        )

    def register(self, login: str, password: str) -> str | int:
        id = self._db.createUser(login, password)
        if id == -1:
            return -1
        return self.login(login, password)


if __name__ == "__main__":
    d = Database(":memory:")
    a = Auth(d)
    jwt = a.register("Kivi", "Gibson")
    if type(jwt) is str:
        print(a.checkCredentials(jwt))
    print("Womp Womp")

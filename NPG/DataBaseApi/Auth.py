import jwt
from .DatabaseApi import Database
import bcrypt


class Auth:
    def __init__(self, db: Database) -> None:
        self._db = db

    def check_credentials(self, token: str | None) -> int:
        if token is None:
            print("No token")
            return -418
        data = jwt.decode(token, "passphrase", algorithms=["HS256"])
        user_id, hash_password = self._db.getUser(data["login"])
        return (
            user_id
            if bcrypt.checkpw(
                bytes(data["password"], "utf-8"), hash_password.encode("utf-8")
            )
            else -404
        )

    def login(self, login: str, password: str) -> str | int:
        res = self._db.getUser(login)
        if res == -404 or not bcrypt.checkpw(
            bytes(password, "utf-8"), res[1].encode("utf-8")
        ):
            return -404
        return jwt.encode(
            {"login": login, "password": password}, "passphrase", algorithm="HS256"
        )

    def register(self, login: str, password: str) -> str | int:
        id = self._db.createUser(
            login,
            bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt()).decode("utf-8"),
        )
        if id == -400:
            return -400
        return self.login(login, password)

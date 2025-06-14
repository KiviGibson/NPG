from flask import Flask, request, Response, make_response
from NPG import Database, PressureData, Auth
import json

app = Flask(__name__)
base = Database("test.db")
auth = Auth(base)


@app.route("/login", methods=["POST"])
def login() -> Response:
    data = request.data
    print(data)
    try:
        cred = auth.login(data["login"], data["password"])
    except Exception:
        return make_response({"status": "bad request"}, 400)
    if cred == -404:
        return make_response(
            {"error": 404, "message": "cant find pair of user and passowrd"}, 404
        )
    res = make_response({"status": "OK"}, 200)
    res.set_cookie("JWT", cred)
    return res


@app.route("/register", methods=["POST"])
def reguister() -> Response:
    data = json.loads(request.data)
    print(data)
    try:
        cred = auth.register(data["login"], data["password"])
        print(cred)
    except ZeroDivisionError:
        return make_response({"status": "bad request"}, 400)
    if cred == -400:
        return make_response({"error": 400, "message": "Login is taken"}, 5000)
    res = make_response({"status": "OK"}, 200)
    res.set_cookie("JWT", cred)
    return res


@app.route("/get_data")
def get_data() -> Response:
    jwt = request.cookies["JWT"]
    id = auth.check_credentials(jwt)
    if id == -403:
        return make_response({"status": "Making Coffee", "message": "im a teepod"}, 418)
    try:
        res_data = [
            {"sys": a.value[0], "dys": a.value[1], "pulse": a.value[2], "date": a.date}
            for a in base.get_data(id, request.data["filters"])
        ]
    except Exception:
        return make_response(
            {"status": "Request denied", "message": "Unexpected error oddured"}, 500
        )
    return make_response({"status": "OK", "data": res_data}, 200)


@app.route("/add_data")
def add_data() -> Response:
    jwt = request.cookies["JWT"]
    id = auth.check_credentials(jwt)
    if id == -403:
        return make_response(
            {"status": "Making Coffee", "message": "I'm a Teepod"}, 418
        )
    try:
        data = PressureData()
        base.addData(data)
    except Exception:
        return make_response(
            {
                "status": "Request denied",
                "message": "Data send was not correctly prepted",
            },
            400,
        )
    return make_response({"status": "OK"}, 200)

from flask import Flask, request, Response, make_response
from NPG import Database, PressureData, Auth
import json

app = Flask(__name__)
base = Database("test.db")
auth = Auth(base)


@app.route("/login", methods=["POST"])
def login() -> Response:
    data = json.loads(request.data)
    try:
        cred = auth.login(data["login"], data["password"])
    except Exception:
        return make_response({"status": "bad request"}, 400)
    if isinstance(cred, int):
        return make_response(
            {"error": 404, "message": "cant find pair of user and passowrd"}, 404
        )
    res = make_response({"status": "OK"}, 200)
    res.set_cookie("JWT", cred)
    return res


@app.route("/register", methods=["POST"])
def reguister() -> Response:
    data = json.loads(request.data)
    try:
        cred = auth.register(data["login"], data["password"])
        print(cred)
    except Exception:
        return make_response({"status": "bad request"}, 400)
    if isinstance(cred, int):
        return make_response({"error": 400, "message": "Login is taken"}, 400)
    res = make_response({"status": "OK"}, 200)
    res.set_cookie("JWT", cred)
    return res


@app.route("/get_data", methods=["POST"])
def get_data() -> Response:
    jwt = request.cookies["JWT"]
    data = json.loads(request.data)
    print(jwt)
    id = auth.check_credentials(jwt)
    print(id, data)
    if id == -403:
        return make_response({"status": "Making Coffee", "message": "im a teepod"}, 418)
    try:
        res_data = [
            {"sys": a.value[0], "dys": a.value[1], "pulse": a.value[2], "date": a.date}
            for a in base.getData(id, data["filters"])
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
    data = json.loads(request.data)
    if id == -403:
        return make_response(
            {"status": "Making Coffee", "message": "I'm a Teepod"}, 418
        )
    try:
        data = PressureData(
            data["date"],
            [data["sys"], data["dys"], data["pulse"]],
            data["desc"] if "desc" in data else "No Description",
        )
        base.addData(id, data)
    except Exception:
        return make_response(
            {
                "status": "Request denied",
                "message": "Data send was not correctly prepted",
            },
            400,
        )
    return make_response({"status": "OK"}, 200)

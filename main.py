from flask import Flask, request, Response, make_response
from NPG import Database, PressureData, Auth

app = Flask(__name__)
base = Database(":memory:")
auth = Auth(base)


@app.route("/login")
def login() -> Response:
    data = request.form
    cred = auth.login(data["login"], data["password"])
    if cred == -404:
        return make_response(
            {"error": 404, "message": "cant find pair of user and passowrd"}, 404
        )
    res = make_response({"status": "OK"}, 200)
    res.set_cookie("JWT", cred)
    return res


@app.route("/reguister")
def reguister() -> Response:
    data = request.form
    cred = auth.register(data["login"], data["password"])
    if cred == -400:
        return make_response({"error": 400, "message": "Login is taken"}, 400)
    res = make_response({"status": "OK"}, 200)
    res.set_cookie("JWT", cred)
    return res


@app.route("/get_data")
def get_data() -> Response:
    jwt = request.cookies["JWT"]
    id = auth.check_credentials(jwt)
    if id == -403:
        return make_response({"status": "Making Coffee", "message": "im a teepod"}, 418)
    res_data = [
        {"sys": "", "dys": "", "pulse": "", "date": ""}
        for a in base.get_data(id, request.form["filters"])
    ]
    return make_response({"status": "OK", "data": res_data}, 200)

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/get_data/<date>/<value>',methods=['GET'])
def get_data(date:tuple[int,int],value:dict[str,tuple]):
    return {"body":[
        {"date":17491206316,"value":[120,80,70],"desc":"Nice"}
    ]}

@app.route('/add_data',methods=['POST'])
def add_data():
    request_data = request.form

    return {"Status":"OK"}

@app.route('/login',methods=['POST'])
def login():
    request_data = request.form
    return {"Status":"OK"}

@app.route('/register',methods=['POST'])
def register():
    request_data = request.form
    return {"Status":"OK"}
from flask import Flask, request, jsonify

app = Flask(_name_)

# Tymczasowe magazyny danych
users = {}  # login -> password
data_storage = []  # lista słowników z danymi

@app.route('/register', methods=['POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return 'missing login or password', 400

    users[login] = password
    return 'ok'

@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if users.get(login) == password:
        return 'ok'
    return 'unauthorized', 401

@app.route('/add_data', methods=['POST'])
def add_data():
    date = request.form.get('date')
    value = request.form.get('value')
    desc = request.form.get('desc')

    if not date or not value or not desc:
        return 'missing fields', 400

    try:
        value = float(value)
    except ValueError:
        return 'invalid value', 400

    data_storage.append({
        'date': date,
        'value': value,
        'desc': desc
    })
    return 'ok'

@app.route('/get_data', methods=['GET'])
def get_data():
    date = request.args.get('date')
    value = request.args.get('value')

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({'data': []})

    # Filtrowanie po dacie i wartości
    filtered_data = [
        entry for entry in data_storage
        if entry['date'] == date and entry['value'] == value
    ]

    return jsonify({'data': filtered_data})

if _name_ == '_main_':
    app.run(debug=True)
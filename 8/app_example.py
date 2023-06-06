from flask import Flask, request, jsonify
import sqlite3
import bcrypt
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       login TEXT UNIQUE NOT NULL,
                       password_hash TEXT NOT NULL,
                       registration_date TEXT NOT NULL)''')
    conn.commit()
    conn.close()


@app.route('/user/', methods=['POST'])
def create_user():
    data = request.get_json()
    login = data['login']
    password = data['password']
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (login, password_hash, registration_date) VALUES (?, ?, ?)",
                       (login, password_hash, registration_date))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "User created"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "User already exists"}), 400


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

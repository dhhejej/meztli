from flask import Blueprint, request, jsonify, session
from services.db import get_connection
from services.security import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM usuarios WHERE usuario=%s", (data['user'],))
    user = cur.fetchone()

    cur.close()
    db.close()

    if user and verify_password(data['pwd'], user['password']):
        session['user'] = user['usuario']
        return jsonify({"status": "success"})

    return jsonify({"status": "error"}), 401

@auth_bp.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.json
    hashed = hash_password(data['pwd'])

    db = get_connection()
    cur = db.cursor()
    cur.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
                (data['user'], hashed))
    db.commit()

    cur.close()
    db.close()

    return jsonify({"status": "success"})

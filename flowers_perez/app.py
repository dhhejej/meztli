from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
import datetime

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234",
            database="rancho",
            port=3309
        )
        return conn
    except Error as e:
        print(f"❌ ERROR MYSQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    u = str(data.get('user', '')).strip()
    p = str(data.get('pwd', '')).strip()

    db = get_db_connection()
    if not db: return jsonify({"status": "error"}), 500

    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE BINARY usuario = %s AND BINARY password = %s", (u, p))
    user = cur.fetchone()
    cur.close()
    db.close()

    return jsonify({"status": "success"}) if user else (jsonify({"status": "error"}), 401)

@app.route('/guardar/<categoria>', methods=['POST'])
def guardar(categoria):
    data = request.json
    db = get_db_connection()
    cur = db.cursor()
    
    try:
        if categoria == 'clientes':
            cur.execute("INSERT INTO clientes (nombre, contacto) VALUES (%s, %s)", (data['nombre'], data['contacto']))
        elif categoria == 'flores':
            cur.execute("INSERT INTO flores (nombre, cantidad) VALUES (%s, %s)", (data['nombre'], data['cantidad']))
        elif categoria == 'materiales':
            cur.execute("INSERT INTO materiales (nombre, cantidad, precio) VALUES (%s, %s, %s)", (data['nombre'], data['cantidad'], data['precio']))
        elif categoria == 'fumigos':
            cur.execute("INSERT INTO fumigos (nombre, cantidad, precio) VALUES (%s, %s, %s)", (data['nombre'], data['cantidad'], data['precio']))
        elif categoria == 'ventas':
            fecha = datetime.datetime.now()
            cur.execute("INSERT INTO ventas (cliente_id, flor_id, cantidad, total, fecha) VALUES (%s, %s, %s, %s, %s)", 
                        (data['cliente_id'], data['flor_id'], data['cantidad'], data['total'], fecha))
        db.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cur.close()
        db.close()

@app.route('/reporte/<categoria>')
def reporte(categoria):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    # Ordenamos por ID descendente para ver lo más nuevo primero, excepto ventas (por fecha)
    order_by = "fecha ASC" if categoria == "ventas" else "id DESC"
    cur.execute(f"SELECT * FROM {categoria} ORDER BY {order_by}")
    resultados = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(resultados)

@app.route('/eliminar/<categoria>/<int:item_id>', methods=['DELETE'])
def eliminar(categoria, item_id):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(f"DELETE FROM {categoria} WHERE id = %s", (item_id,))
    db.commit()
    cur.close()
    db.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
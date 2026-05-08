from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
import datetime

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234",
            database="flower",
            port=3306
        )
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    u, p = data.get('user', '').strip(), data.get('pwd', '').strip()
    db = get_db_connection()
    if not db: return jsonify({"status": "error"}), 500
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE BINARY usuario = %s AND BINARY password = %s", (u, p))
    user = cur.fetchone()
    cur.close()
    db.close()
    return jsonify({"status": "success"}) if user else (jsonify({"status": "error"}), 401)

@app.route('/guardar/<categoria>', methods=['POST'])
def guardar_datos(categoria):
    data = request.json
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        if categoria == 'flores':
            cur.execute("INSERT INTO flores (nombre, tipo, variedad, cantidad) VALUES (%s, %s, %s, %s)", 
                        (data['nombre'], data['tipo'], data['variedad'], data['cantidad']))
        elif categoria == 'ventas':
            cur.execute("SELECT cantidad FROM flores WHERE id = %s", (data['flor_id'],))
            flor = cur.fetchone()
            if not flor or flor['cantidad'] < int(data['cantidad']):
                return jsonify({"status": "error", "message": "Stock insuficiente"}), 400
            cur.execute("INSERT INTO ventas (cliente_id, flor_id, cantidad, total, fecha) VALUES (%s, %s, %s, %s, %s)", 
                        (data['cliente_id'], data['flor_id'], data['cantidad'], data['total'], datetime.datetime.now()))
            cur.execute("UPDATE flores SET cantidad = cantidad - %s WHERE id = %s", (data['cantidad'], data['flor_id']))
        elif categoria == 'clientes':
            cur.execute("INSERT INTO clientes (nombre, contacto) VALUES (%s, %s)", (data['nombre'], data['contacto']))
        elif categoria in ['materiales', 'fumigos']:
            cur.execute(f"INSERT INTO {categoria} (nombre, cantidad, precio) VALUES (%s, %s, %s)", 
                        (data['nombre'], data['cantidad'], data['precio']))
        db.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cur.close()
        db.close()

@app.route('/reporte/<categoria>')
def reporte(categoria):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    
    if categoria == 'ventas':
        # Consulta con JOIN para obtener nombres en lugar de IDs
        query = """
            SELECT 
                v.id AS ID, 
                c.nombre AS CLIENTE, 
                f.nombre AS FLOR, 
                v.cantidad AS CANTIDAD, 
                v.total AS TOTAL, 
                v.fecha AS FECHA 
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN flores f ON v.flor_id = f.id
            ORDER BY v.id DESC
        """
        cur.execute(query)
    else:
        cur.execute(f"SELECT * FROM {categoria} ORDER BY id DESC")
        
    res = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(res)

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
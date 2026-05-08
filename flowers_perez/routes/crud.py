from flask import Blueprint, request, jsonify, session
from services.db import get_connection
import datetime

crud_bp = Blueprint('crud', __name__)

def protegido():
    return 'user' in session

@crud_bp.route('/guardar/<categoria>', methods=['POST'])
def guardar(categoria):
    if not protegido():
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    db = get_connection()
    cur = db.cursor()

    if categoria == 'clientes':
        cur.execute("INSERT INTO clientes (nombre, contacto) VALUES (%s,%s)",
                    (data['nombre'], data['contacto']))

    elif categoria == 'ventas':
        fecha = datetime.datetime.now()
        cur.execute("UPDATE flores SET cantidad = cantidad - %s WHERE id=%s",
                    (data['cantidad'], data['flor_id']))
        cur.execute("INSERT INTO ventas (cliente_id, flor_id, cantidad, total, fecha) VALUES (%s,%s,%s,%s,%s)",
                    (data['cliente_id'], data['flor_id'], data['cantidad'], data['total'], fecha))

    db.commit()
    cur.close()
    db.close()

    return jsonify({"status": "success"})

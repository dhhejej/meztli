from flask import Blueprint, jsonify, session
from services.db import get_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return jsonify({"error": "No autorizado"}), 403

    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS clientes FROM clientes")
    clientes = cur.fetchone()['clientes']

    cur.execute("SELECT COUNT(*) AS ventas FROM ventas")
    ventas = cur.fetchone()['ventas']

    cur.execute("SELECT SUM(total) AS ingresos FROM ventas")
    ingresos = cur.fetchone()['ingresos'] or 0

    cur.close()
    db.close()

    return jsonify({
        "clientes": clientes,
        "ventas": ventas,
        "ingresos": ingresos
    })

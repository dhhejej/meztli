from flask import Blueprint, jsonify, session
from services.db import get_connection

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reporte/<categoria>')
def reporte(categoria):
    if 'user' not in session:
        return jsonify([])

    db = get_connection()
    cur = db.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM {categoria}")
    data = cur.fetchall()

    cur.close()
    db.close()

    return jsonify(data)

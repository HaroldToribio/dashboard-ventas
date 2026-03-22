from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from typing import Union, Tuple

from backend.repositories.ventas_repository import VentasRepository
from backend.data_loader import cargar_datos
from backend.services.prediccion_service import predecir_demanda

app = Flask(__name__)
CORS(app)

repo = VentasRepository()

# =========================
# PRODUCTOS
# =========================

@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        data = repo.get_productos()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.json

        nombre          = data.get('nombre')
        precio          = data.get('precio')
        promedio_ventas = data.get('promedio_ventas')  # estimado por el usuario

        if not nombre or precio is None:
            return jsonify({"error": "Nombre y precio son requeridos"}), 400

        nuevo_id = repo.crear_producto(nombre, precio)

        # Si el usuario ingresó un promedio, generamos historial simulado
        if promedio_ventas and int(promedio_ventas) > 0 and nuevo_id:
            repo.simular_ventas_historicas(nuevo_id, int(promedio_ventas), dias=90)

        return jsonify({"mensaje": "Producto creado", "id_producto": nuevo_id}), 201

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# =========================
# DELETE
# =========================
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        repo.eliminar_producto(id)
        return jsonify({"mensaje": "Producto eliminado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# VENTAS
# =========================

@app.route('/ventas', methods=['GET'])
def obtener_ventas_general():
    try:
        data = repo.obtener_ventas()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/ventas/<int:id_producto>')
def obtener_ventas(id_producto):
    try:
        ventas = repo.obtener_ventas_por_producto(id_producto)
        return jsonify(ventas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ventas-por-producto', methods=['GET'])
def ventas_por_producto():
    try:
        data = repo.obtener_resumen_ventas()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# PREDICCION
# =========================
@app.route('/prediccion/<int:producto_id>')
def obtener_prediccion(producto_id):
    try:
        dias = request.args.get('dias', default=7, type=int)
        df = cargar_datos(producto_id)
        resultado = predecir_demanda(df, dias=dias)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():
    try:
        producto = request.args.get('producto', type=int)
        dias = request.args.get('dias', type=int)

        if not producto or not dias:
            return jsonify({"error": "Parámetros inválidos"}), 400

        data = repo.get_dashboard(producto, dias)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return {
        "mensaje": "API funcionando",
        "endpoints": ["/productos", "/dashboard"]
    }


if __name__ == '__main__':
    app.run(debug=True)
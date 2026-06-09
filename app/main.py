from flask import Flask, request, jsonify, render_template
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
import os
import decimal

load_dotenv()


class StockFlowJSONProvider(DefaultJSONProvider):
    @staticmethod
    def default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(StockFlowJSONProvider, StockFlowJSONProvider).default(obj)


app = Flask(__name__, static_url_path="")
app.json = StockFlowJSONProvider(app)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


# =========================
# CONFIGURACIÓN DE BD
# =========================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "stockflow_db"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# =========================
# RUTAS - PRODUCTOS
# =========================

# GET /api/products — listar todos los productos
@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products ORDER BY name ASC")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/products/<id> — obtener un producto por ID
@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        if not product:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST /api/products — crear un nuevo producto
@app.route("/api/products", methods=["POST"])
def create_product():
    try:
        data = request.get_json()
        required = ["name", "category", "stock", "minimum_stock", "price"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"El campo '{field}' es requerido"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO products (name, category, stock, minimum_stock, price)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data["name"],
            data["category"],
            data["stock"],
            data["minimum_stock"],
            data["price"],
        )
        cursor.execute(sql, values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Producto creado exitosamente", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT /api/products/<id> — actualizar un producto
@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        data = request.get_json()
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Verificar que existe
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404

        # Mezclar valores actuales con los nuevos (PATCH-style dentro de PUT)
        name = data.get("name", product["name"])
        category = data.get("category", product["category"])
        stock = data.get("stock", product["stock"])
        minimum_stock = data.get("minimum_stock", product["minimum_stock"])
        price = data.get("price", product["price"])

        sql = """
            UPDATE products
            SET name = %s, category = %s, stock = %s, minimum_stock = %s, price = %s
            WHERE id = %s
        """
        cursor.execute(sql, (name, category, stock, minimum_stock, price, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT /api/products/<id>/stock — agregar stock (desde el modal)
@app.route("/api/products/<int:product_id>/stock", methods=["PUT"])
def add_stock(product_id):
    try:
        data = request.get_json()
        if "amount" not in data or int(data["amount"]) <= 0:
            return jsonify({"error": "La cantidad debe ser un número positivo"}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404

        sql = "UPDATE products SET stock = stock + %s WHERE id = %s"
        cursor.execute(sql, (int(data["amount"]), product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Stock actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE /api/products/<id> — eliminar un producto
@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404

        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# INICIO
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=5000)

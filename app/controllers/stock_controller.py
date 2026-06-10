from flask import request, jsonify
from flask.views import MethodView

from ..repositories.product_repository import ProductRepository


class StockController(MethodView):
    def __init__(self, repository: ProductRepository):
        self._repo = repository

    def put(self, product_id: int):
        try:
            data = request.get_json()
            if "amount" not in data or int(data["amount"]) <= 0:
                return jsonify(
                    {"error": "La cantidad debe ser un número positivo"}
                ), 400

            existing = self._repo.find_by_id(product_id)
            if not existing:
                return jsonify({"error": "Producto no encontrado"}), 404

            self._repo.add_stock(product_id, int(data["amount"]))
            return jsonify(
                {"message": "Stock actualizado exitosamente"}
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

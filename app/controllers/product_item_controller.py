from flask import request, jsonify
from flask.views import MethodView
from decimal import Decimal

from ..repositories.product_repository import ProductRepository


class ProductItemController(MethodView):
    def __init__(self, repository: ProductRepository):
        self._repo = repository

    def get(self, product_id: int):
        try:
            product = self._repo.find_by_id(product_id)
            if not product:
                return jsonify({"error": "Producto no encontrado"}), 404
            return jsonify(product.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, product_id: int):
        try:
            existing = self._repo.find_by_id(product_id)
            if not existing:
                return jsonify({"error": "Producto no encontrado"}), 404

            data = request.get_json()
            existing.name = data.get("name", existing.name)
            existing.category = data.get("category", existing.category)
            existing.stock = int(data.get("stock", existing.stock))
            existing.minimum_stock = int(
                data.get("minimum_stock", existing.minimum_stock)
            )
            raw_price = data.get("price", existing.price)
            existing.price = (
                Decimal(str(raw_price)) if raw_price is not None
                else existing.price
            )

            self._repo.update(existing)
            return jsonify(
                {"message": "Producto actualizado exitosamente"}
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, product_id: int):
        try:
            existing = self._repo.find_by_id(product_id)
            if not existing:
                return jsonify({"error": "Producto no encontrado"}), 404
            self._repo.delete(product_id)
            return jsonify(
                {"message": "Producto eliminado exitosamente"}
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

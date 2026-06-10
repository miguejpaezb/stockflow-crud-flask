from flask import request, jsonify
from flask.views import MethodView
from decimal import Decimal

from ..models.product import Product
from ..repositories.product_repository import ProductRepository


class ProductListController(MethodView):
    def __init__(self, repository: ProductRepository):
        self._repo = repository

    def get(self):
        try:
            products = self._repo.find_all()
            return jsonify([p.to_dict() for p in products]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            required = ["name", "category", "stock", "minimum_stock", "price"]
            for field in required:
                if field not in data:
                    return jsonify(
                        {"error": f"El campo '{field}' es requerido"}
                    ), 400

            product = Product(
                name=data["name"],
                category=data["category"],
                stock=int(data["stock"]),
                minimum_stock=int(data["minimum_stock"]),
                price=Decimal(str(data["price"])),
            )
            new_id = self._repo.create(product)
            return jsonify(
                {"message": "Producto creado exitosamente", "id": new_id}
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

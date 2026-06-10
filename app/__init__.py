from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from .config import Config
from .database import Database
from .json_provider import StockFlowJSONProvider
from .repositories.product_repository import ProductRepository
from .controllers.product_list_controller import ProductListController
from .controllers.product_item_controller import ProductItemController
from .controllers.stock_controller import StockController

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="")
    app.json = StockFlowJSONProvider(app)
    CORS(app)

    config = Config()
    database = Database(config)
    repository = ProductRepository(database)

    product_list = ProductListController.as_view(
        "product_list", repository
    )
    product_item = ProductItemController.as_view(
        "product_item", repository
    )
    stock = StockController.as_view(
        "stock", repository
    )

    app.add_url_rule(
        "/api/products",
        view_func=product_list,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/api/products/<int:product_id>",
        view_func=product_item,
        methods=["GET", "PUT", "DELETE"],
    )
    app.add_url_rule(
        "/api/products/<int:product_id>/stock",
        view_func=stock,
        methods=["PUT"],
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

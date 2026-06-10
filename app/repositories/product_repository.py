from ..database import Database
from ..models.product import Product


class ProductRepository:
    def __init__(self, database: Database):
        self._db = database

    def find_all(self) -> list[Product]:
        conn = self._db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products ORDER BY name ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Product.from_row(row) for row in rows]

    def find_by_id(self, product_id: int) -> Product | None:
        conn = self._db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return Product.from_row(row)

    def create(self, product: Product) -> int:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO products (name, category, stock, minimum_stock, price)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (product.name, product.category, product.stock,
             product.minimum_stock, product.price),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        product.id = new_id
        return new_id

    def update(self, product: Product) -> None:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE products
            SET name = %s, category = %s, stock = %s,
                minimum_stock = %s, price = %s
            WHERE id = %s
        """
        cursor.execute(
            sql,
            (product.name, product.category, product.stock,
             product.minimum_stock, product.price, product.id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def add_stock(self, product_id: int, amount: int) -> None:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET stock = stock + %s WHERE id = %s",
            (amount, product_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, product_id: int) -> None:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()

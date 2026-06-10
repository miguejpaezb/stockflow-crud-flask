from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Product:
    name: str
    category: str
    stock: int = 0
    minimum_stock: int = 1
    price: Decimal = Decimal("0.00")
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict) -> "Product":
        return cls(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            stock=row["stock"],
            minimum_stock=row["minimum_stock"],
            price=row["price"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "stock": self.stock,
            "minimum_stock": self.minimum_stock,
            "price": self.price,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }

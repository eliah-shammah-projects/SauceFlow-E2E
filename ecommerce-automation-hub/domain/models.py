from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Product:
    id: str
    title: str
    price: float
    currency: str
    url: str
    source: str


@dataclass
class Cart:
    items: List[Product] = field(default_factory=list)

    def add(self, product: Product) -> None:
        self.items.append(product)

    def remove(self, product_id: str) -> None:
        self.items = [p for p in self.items if p.id != product_id]

    @property
    def total(self) -> float:
        return sum(p.price for p in self.items)


@dataclass
class Order:
    items: List[Product]
    total: float
    success: bool
    screenshot_path: Optional[str] = None
    error: Optional[str] = None

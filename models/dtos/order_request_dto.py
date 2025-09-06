from dataclasses import dataclass

@dataclass
class OrderRequestDTO:
	customer_id: str
	product_id: str
	quantity: int
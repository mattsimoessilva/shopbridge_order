from dataclasses import dataclass

@dataclass
class OrderResponseDTO:
	id: str
	customer_id: str
	product_id: str
	quantity: int
	status: str
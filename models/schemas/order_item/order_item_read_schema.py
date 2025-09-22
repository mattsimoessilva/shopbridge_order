from marshmallow import Schema, fields, post_dump

class OrderItemReadSchema(Schema):
    product_id = fields.UUID(required=True, metadata={"description": "Product's unique identifier"})
    product_variant_id = fields.UUID(required=False, metadata={"description": "Product Variant's unique identifier"})
    quantity = fields.Integer(required=True, metadata={"description": "Quantity of the product ordered"})
    unit_price = fields.Float(allow_none=True, metadata={"description": "Unit price of the product"})
    total_price = fields.Float(dump_only=True, metadata={"description": "Total price (quantity times unit_price)"})

    @post_dump
    def calculate_total_price(self, data, **kwargs):
        unit_price = data.get("unit_price")
        quantity = data.get("quantity")
        if unit_price is not None and quantity is not None:
            data["total_price"] = round(unit_price * quantity, 2)
        else:
            data["total_price"] = None
        return data
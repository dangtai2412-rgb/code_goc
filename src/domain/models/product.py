# src/domain/models/product.py

class Product:
    def __init__(self, product_name, owner_id, selling_price, stock_quantity, 
                 sku=None, category_id=None, unit_id=None, product_id=None):
        self.product_id = product_id
        self.product_name = product_name
        self.owner_id = owner_id
        self.selling_price = selling_price
        self.stock_quantity = stock_quantity
        self.sku = sku  # BỔ SUNG DÒNG NÀY
        self.category_id = category_id
        self.unit_id = unit_id
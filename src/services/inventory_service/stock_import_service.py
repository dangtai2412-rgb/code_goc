from infrastructure.models.inventory.stock_import_model import StockImportModel
from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel

class StockImportService:
    def __init__(self, import_repo, detail_repo, product_repo):
        self.import_repo = import_repo
        self.detail_repo = detail_repo
        self.product_repo = product_repo

    # src/services/inventory_service/stock_import_service.py


    # ĐỔI TÊN HÀM TỪ create_import_ticket THÀNH create_stock_import
    def create_stock_import(self, data, owner_id): 
        try:
            # 1. Tạo Header cho phiếu nhập
            new_import = StockImportModel(
                owner_id=owner_id,
                supplier_id=data.get('supplier_id'),
                total_amount=data.get('total_amount', 0),
                import_date=data.get('import_date')
            )
            self.import_repo.add(new_import)

            # 2. Duyệt qua danh sách hàng nhập (SỬA 'details' THÀNH 'items' cho khớp Swagger)
            for item in data.get('items', []):
                detail = StockImportDetailModel(
                    import_id=new_import.import_id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['import_price'],
                    line_total=item['quantity'] * item['import_price']
                )
                self.detail_repo.add(detail)

                # CẬP NHẬT KHO
                product = self.product_repo.get_by_id(item['product_id'])
                if product:
                    product.stock_quantity = (product.stock_quantity or 0) + item['quantity']
            
            # 3. Lưu vào DB
            self.import_repo.session.commit() 
            return new_import
            
        except Exception as e:
            self.import_repo.session.rollback()
            raise e
    def get_history_by_owner(self, owner_id):
        # SỬA TẠI ĐÂY: Dùng self.import_repo thay vì self.repository
        return self.import_repo.get_all_by_owner(owner_id)
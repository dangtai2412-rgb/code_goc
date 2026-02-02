# src/dependency_container.py
# ... (Giữ nguyên các imports khác)

    # Tìm đến phần đăng ký order_service và sửa lại như sau:
    order_service = providers.Factory(
        OrderService,  
        order_repo=order_repository, 
        order_detail_repo=order_detail_repository, # Thêm cái này
        product_repo=product_repository, 
        debt_service=debt_service,
        db=db_session_provider # Thêm cái này để quản lý Transaction
    )
import logging

def setup_logging(app=None): # Thêm app=None ở đây
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    # Nếu có truyền app vào, có thể log thông báo khởi tạo
    if app:
        app.logger.info("Logging has been initialized for the Flask app.")


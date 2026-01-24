from create_app import create_app
from infrastructure.databases.base import Base
from infrastructure.databases.mssql import engine
from flask_migrate import Migrate
# Gọi hàm create_app duy nhất từ file create_app.py
app = create_app()

if __name__ == '__main__':
    # Chạy trên port bạn mong muốn (ví dụ 9999 như file cũ của bạn)
    app.run(host='0.0.0.0', port=9999, debug=True)

class SQLAlchemyPatcher:
    def __init__(self, metadata, engine):
        self.metadata = metadata
        self.engine = engine


db_wrapper = SQLAlchemyPatcher(Base.metadata, engine)
migrate = Migrate(app, Base.metadata)



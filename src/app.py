from create_app import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from infrastructure.databases.mssql import db

# Gọi hàm create_app duy nhất từ file create_app.py
app = create_app()

if __name__ == '__main__':
    # Chạy trên port bạn mong muốn (ví dụ 9999 như file cũ của bạn)
    app.run(host='0.0.0.0', port=9999, debug=True)


migrate = Migrate(app, db)
-- Kiểm tra xem cột có IDENTITY không. Nếu không có, bạn nên xóa bảng và tạo lại:
DROP TABLE stock_import_details;

CREATE TABLE stock_import_details (
    detail_id INT PRIMARY KEY IDENTITY(1,1), -- BẮT BUỘC PHẢI CÓ IDENTITY
    import_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    line_total DECIMAL(18,2) NULL, -- Nên thêm cột này luôn để tránh lỗi invalid keyword
    CONSTRAINT FK_Detail_Import FOREIGN KEY (import_id) REFERENCES stock_imports(import_id),
    CONSTRAINT FK_Detail_Product FOREIGN KEY (product_id) REFERENCES products(product_id)
);
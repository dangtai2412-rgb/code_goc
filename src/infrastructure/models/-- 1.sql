-- 1. Tạo Database mới tên là FlaskApiDB (khớp với file config.py của bạn)
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'FlaskApiDB')
BEGIN
    CREATE DATABASE FlaskApiDB;
    PRINT 'Da tao Database FlaskApiDB thanh cong.';
END
ELSE
BEGIN
    PRINT 'Database FlaskApiDB da ton tai.';
END
GO
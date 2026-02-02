from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

employee_bp = Blueprint('employee_bp', __name__)

# --- 1. TẠO NHÂN VIÊN (Chỉ Owner mới có quyền) ---
@employee_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_employee(emp_service = Provide[Container.employee_service]):
    """
    Tạo nhân viên mới (Gán trực tiếp vào shop của Owner)
    """
    try:
        data = request.get_json()
        
        # Lấy thông tin user từ Middleware
        current_user = getattr(request, 'current_user', {})
        # Quan trọng: Kiểm tra xem người gọi có phải là CHỦ SHOP không
        if current_user.get('role') != 'owner':
            return jsonify({"error": "Chỉ chủ cửa hàng mới có quyền tạo nhân viên"}), 403

        owner_id = current_user.get('id')
        
        # Service sẽ xử lý: Hash mật khẩu, kiểm tra email trùng, gán owner_id vào record employee
        result = emp_service.create_employee(data, owner_id)
        
        return jsonify({
            "message": "Thành công", 
            "employee_id": result.employee_id
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Lỗi hệ thống khi tạo nhân viên"}), 500

# --- 2. LIẾT KÊ NHÂN VIÊN (Theo Shop của Owner) ---
@employee_bp.route('/', methods=['GET'])
@token_required
@inject
def list_employees(emp_service = Provide[Container.employee_service]):
    """
    Lấy danh sách nhân viên thuộc quyền quản lý của Owner hiện tại
    """
    try:
        current_user = getattr(request, 'current_user', {})
        owner_id = current_user.get('id')
        
        # Chỉ lấy nhân viên của chính shop này
        employees = emp_service.get_employees_by_owner(owner_id)
        
        return jsonify([
            {
                "id": e.employee_id, 
                "name": e.employee_name, 
                "role": e.role, 
                "email": e.email,
                "status": getattr(e, 'status', 'active') # Trạng thái làm việc
            } 
            for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": "Không thể lấy danh sách nhân viên"}), 500

# --- 3. XÓA/VÔ HIỆU HÓA NHÂN VIÊN ---
@employee_bp.route('/<int:emp_id>', methods=['DELETE'])
@token_required
@inject
def remove_employee(emp_id, emp_service = Provide[Container.employee_service]):
    """ Vô hiệu hóa quyền truy cập của nhân viên """
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        
        # Service cần kiểm tra xem emp_id này có thực sự thuộc về owner_id này không
        success = emp_service.delete_employee(emp_id, owner_id)
        
        if not success:
            return jsonify({"error": "Không tìm thấy nhân viên hoặc bạn không có quyền"}), 404
            
        return jsonify({"message": "Đã xóa nhân viên thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
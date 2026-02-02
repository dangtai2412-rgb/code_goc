from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

employee_bp = Blueprint('employee_bp', __name__)

# --- 1. TẠO NHÂN VIÊN (Bổ sung Check Quota & Branch) ---
@employee_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_employee(emp_service = Provide[Container.employee_service]):
    try:
        data = request.get_json()
        current_user = getattr(request, 'current_user', {})
        
        if current_user.get('role') != 'owner':
            return jsonify({"error": "Quyền này chỉ dành cho chủ sở hữu"}), 403

        owner_id = current_user.get('id')
        
        # LOGIC NÂNG CAO: Kiểm tra số lượng nhân viên tối đa của gói cước
        # current_count = emp_service.count_employees(owner_id)
        # if current_count >= current_user.get('max_employees'):
        #     return jsonify({"error": "Bạn đã đạt giới hạn nhân viên của gói cước hiện tại"}), 400

        result = emp_service.create_employee(data, owner_id)
        return jsonify({"message": "Thành công", "id": result.employee_id}), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Lỗi hệ thống nội bộ"}), 500

# --- 2. CẬP NHẬT NHÂN VIÊN (Tính năng mới) ---
@employee_bp.route('/<int:emp_id>', methods=['PATCH'])
@token_required
@inject
def update_employee(emp_id, emp_service = Provide[Container.employee_service]):
    """ Cập nhật vai trò hoặc trạng thái nhân viên """
    try:
        data = request.get_json()
        owner_id = getattr(request, 'current_user', {}).get('id')
        
        # Đảm bảo nhân viên thuộc sở hữu của Owner này trước khi sửa
        updated = emp_service.update_employee_info(emp_id, owner_id, data)
        
        if not updated:
            return jsonify({"error": "Không tìm thấy nhân viên"}), 404
            
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- 3. LIÊT KÊ CÓ LỌC (Filter by Branch/Status) ---
@employee_bp.route('/', methods=['GET'])
@token_required
@inject
def list_employees(emp_service = Provide[Container.employee_service]):
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        
        # Lấy thêm các tham số lọc từ URL (ví dụ: ?branch_id=1&status=active)
        branch_id = request.args.get('branch_id', type=int)
        status = request.args.get('status', type=str)
        
        employees = emp_service.get_employees_filtered(owner_id, branch_id, status)
        
        return jsonify([
            {
                "id": e.employee_id, 
                "name": e.employee_name, 
                "role": e.role, 
                "email": e.email,
                "branch_name": getattr(e.branch, 'name', 'N/A') if hasattr(e, 'branch') else None,
                "status": getattr(e, 'status', 'active')
            } 
            for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
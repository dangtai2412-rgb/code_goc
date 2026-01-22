from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.access_and_identity_service.employee_service import EmployeeService
employee_bp = Blueprint('employee_bp', __name__)

# src/api/controllers/access_and_identity_control/employee_controller.py

@employee_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_employee(emp_service = Provide[Container.employee_service]):
    """
    Tạo nhân viên mới
    ---
    tags: [Employee]
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [employee_name, email, password] # KHÔNG CẦN owner_id ở đây nữa
          properties:
            employee_name: {type: string, example: "Nhan Vien A"}
            email: {type: string, example: "nv_a@shop.com"}
            password: {type: string, example: "nv123"}
            role: {type: string, example: "Staff"}
    """
    try:
        data = request.get_json()
        
        # TỰ ĐỘNG LẤY TỪ TOKEN
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
        
        if not owner_id:
            return jsonify({"error": "Bạn phải là chủ cửa hàng để thực hiện hành động này"}), 403

        # Truyền owner_id riêng biệt xuống Service
        result = emp_service.create_employee(data, owner_id)
        return jsonify({"message": "Thành công", "id": result.employee_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_bp.route('/', methods=['GET']) # Bỏ owner_id khỏi URL cho an toàn
@token_required
@inject
def list_employees(emp_service = Provide[Container.employee_service]):
    """
    Lấy danh sách nhân viên của shop hiện tại
    ---
    tags: [Employee]
    security: [{BearerAuth: []}]
    """
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
        
        employees = emp_service.get_employees_by_owner(owner_id)
        return jsonify([
            {"id": e.employee_id, "name": e.employee_name, "role": e.role, "email": e.email} 
            for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
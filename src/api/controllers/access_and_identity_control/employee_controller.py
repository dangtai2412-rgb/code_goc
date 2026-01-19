from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_employee(emp_service = Provide[Container.employee_service]):
    """
    Tạo nhân viên mới (Cho chủ cửa hàng)
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - employee_name
            - email
            - password
            - owner_id
          properties:
            employee_name:
              type: string
              example: "Nhan Vien A"
            email:
              type: string
              example: "nv_a@shop.com"
            phone_number:
              type: string
              example: "0912345678"
            password:
              type: string
              example: "nv123"
            role:
              type: string
              example: "Staff"
              enum: ["Manager", "Staff"]
            owner_id:
              type: integer
              description: ID của chủ cửa hàng quản lý nhân viên này
              example: 1
    responses:
      201:
        description: Tạo thành công
      400:
        description: Lỗi dữ liệu
    """
    try:
        data = request.get_json()
        result = emp_service.create_employee(data)
        return jsonify({"message": "Thành công", "id": result.employee_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_bp.route('/owner/<int:owner_id>', methods=['GET'])
@token_required
@inject
def list_employees_by_owner(owner_id, emp_service = Provide[Container.employee_service]):
    """
    Lấy danh sách nhân viên theo Chủ cửa hàng
    ---
    tags:
      - Employee
    security:
      - Bearer: []
    parameters:
      - in: path
        name: owner_id
        type: integer
        required: true
        description: ID của chủ cửa hàng
    responses:
      200:
        description: Danh sách nhân viên
    """
    try:
        employees = emp_service.get_employees_by_owner(owner_id)
        return jsonify([
            {"id": e.employee_id, "name": e.employee_name, "role": e.role, "email": e.email} 
            for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

subscription_plan_bp = Blueprint('subscription_plan_bp', __name__)

@subscription_plan_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_subscription_plan(plan_service = Provide[Container.subscription_plan_service]):
    """
    Tạo gói cước dịch vụ mới (Admin)
    ---
    tags:
      - Subscription Plan
    security:
      - BearerAuth: []  # <--- FIXED: Match the name in create_app.py
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [plan_name, price, duration]
          properties:
            plan_name: {type: string, example: "Gói Cơ Bản (Basic)"}
            price: {type: number, example: 199000}
            duration: {type: integer, example: 30}
            description: {type: string, example: "Dành cho cửa hàng nhỏ"}
    responses:
      201: {description: "Tạo thành công"}
      400: {description: "Lỗi dữ liệu"}
    """
    try:
        data = request.get_json()
        result = plan_service.create_plan(data)
        return jsonify({"message": "Tạo gói cước thành công", "id": result.plan_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subscription_plan_bp.route('/', methods=['GET'])
@inject
def list_all_plans(plan_service = Provide[Container.subscription_plan_service]):
    """
    Lấy danh sách các gói cước (Public - No token required)
    ---
    tags:
      - Subscription Plan
    responses:
      200:
        description: Danh sách gói cước
    """
    try:
        plans = plan_service.list_plans()
        return jsonify([
            {
                "id": p.plan_id, 
                "name": p.plan_name, 
                "price": float(p.price) if p.price else 0,
                "duration": p.duration_days
            } for p in plans
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
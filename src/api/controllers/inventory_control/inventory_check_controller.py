from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.inventory_service.inventory_check_service import InventoryCheckService
from api.middlewares.auth_middleware import token_required

inventory_check_bp = Blueprint('inventory_check_bp', __name__)

@inventory_check_bp.route('/', methods=['POST'])
@token_required
@inject
def create_check(current_user, service: InventoryCheckService = Provide[Container.inventory_check_service]):
    """
    Tạo phiếu kiểm kho và cập nhật số lượng tồn kho ngay lập tức.
    Body:
    {
        "note": "Kiểm kho cuối tháng",
        "details": [
            {"product_id": 1, "actual_quantity": 50, "reason": "Hư hỏng 2 cái"},
            {"product_id": 2, "actual_quantity": 10, "reason": ""}
        ]
    }
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        data = request.json
        new_check = service.create_check(data, owner_id)
        
        return jsonify({
            "message": "Kiểm kho thành công. Đã cập nhật tồn kho.",
            "check_id": new_check.check_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_check_bp.route('/', methods=['GET'])
@token_required
@inject
def get_history(current_user, service: InventoryCheckService = Provide[Container.inventory_check_service]):
    """
    Lấy lịch sử các phiên kiểm kho
    ---
    tags: [Inventory - Check]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Danh sách các phiếu kiểm
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        checks = service.get_history(owner_id)
        
        # Serialize dữ liệu trả về
        result = []
        for c in checks:
            result.append({
                "check_id": c.check_id,
                "date": c.check_date.strftime("%d/%m/%Y %H:%M"),
                "note": c.note,
                "status": c.status
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inventory_check_bp.route('/<int:check_id>', methods=['GET'])
@token_required
@inject
def get_check_detail(check_id, current_user, service: InventoryCheckService = Provide[Container.inventory_check_service]):
    """
    Xem chi tiết một phiếu kiểm kho
    ---
    tags: [Inventory - Check]
    security: [{BearerAuth: []}]
    parameters:
      - name: check_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Chi tiết phiếu kiểm và chênh lệch
      404:
        description: Không tìm thấy phiếu
    """
    try:
        check = service.get_detail(check_id)
        if not check:
             return jsonify({"message": "Không tìm thấy phiếu kiểm"}), 404
             
        details = [{
            "product_id": d.product_id,
            "system_qty": d.system_quantity,
            "actual_qty": d.actual_quantity,
            "variance": d.variance,
            "reason": d.reason
        } for d in check.details]
        
        return jsonify({
            "check_id": check.check_id,
            "note": check.note,
            "details": details
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
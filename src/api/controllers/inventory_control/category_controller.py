from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.inventory_service.category_service import CategoryService
from api.middlewares.auth_middleware import token_required

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['POST'])
@token_required
@inject
def create_category(current_user, service: CategoryService = Provide[Container.category_service]):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        data = request.json
        
        new_cate = service.create_category(data, owner_id)
        
        return jsonify({
            "message": "Tạo danh mục thành công", 
            "id": new_cate.category_id,
            "name": new_cate.category_name
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@category_bp.route('/', methods=['GET'])
@token_required
@inject
def list_categories(current_user, service: CategoryService = Provide[Container.category_service]):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        categories = service.get_categories(owner_id)
        
        return jsonify([{
            "category_id": c.category_id,
            "category_name": c.category_name,
            "description": c.description
        } for c in categories]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
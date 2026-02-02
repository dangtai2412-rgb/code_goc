from api.controllers.access_and_identity_control.business_owner_controller import business_owner_bp
from api.controllers.access_and_identity_control.employee_controller import employee_bp
from api.controllers.access_and_identity_control.administrator_controller import admin_bp
from api.controllers.access_and_identity_control.subscription_plan_controller import subscription_plan_bp

from api.controllers.auth_controller import auth_bp

from api.controllers.inventory_control.product_controller import product_bp
from api.controllers.inventory_control.category_controller import category_bp
from api.controllers.inventory_control.unit_controller import unit_bp
from api.controllers.inventory_control.supplier_controller import supplier_bp
from api.controllers.inventory_control.stock_import_controller import stock_import_bp
from api.controllers.inventory_control.stock_import_detail_controller import stock_import_detail_bp
from api.controllers.inventory_control.inventory_check_controller import inventory_check_bp

from api.controllers.sale_and_finance_control.customer_controller import customer_bp
from api.controllers.sale_and_finance_control.order_controller import order_bp
from api.controllers.sale_and_finance_control.order_detail_controller import order_detail_bp
from api.controllers.sale_and_finance_control.debt_controller import debt_bp
from api.controllers.sale_and_finance_control.payment_controller import payment_bp
from api.controllers.sale_and_finance_control.account_report_controller import account_report_bp
from api.controllers.sale_and_finance_control.expense_controller import expense_bp
from api.controllers.sale_and_finance_control.return_order_controller import return_order_bp

from api.controllers.ai_core_control.ai_assistant_controller import ai_assistant_bp
from api.controllers.ai_core_control.ai_draft_order_controller import ai_draft_order_bp


ROUTE_GROUPS = [
    (auth_bp, "/api/auth"),

    (business_owner_bp, "/api/business-owners"),
    (employee_bp, "/api/employees"),
    (admin_bp, "/api/administrators"),
    (subscription_plan_bp, "/api/subscription-plans"),

    (product_bp, "/api/products"),
    (category_bp, "/api/categories"),
    (unit_bp, "/api/units"),
    (supplier_bp, "/api/suppliers"),
    (stock_import_bp, "/api/stock-imports"),
    (stock_import_detail_bp, "/api/stock-import-details"),
    (inventory_check_bp, "/api/inventory-checks"),

    (customer_bp, "/api/customers"),
    (order_bp, "/api/orders"),
    (order_detail_bp, "/api/order-details"),
    (debt_bp, "/api/debts"),
    (payment_bp, "/api/payments"),
    (account_report_bp, "/api/account-reports"),
    (expense_bp, "/api/expenses"),
    (return_order_bp, "/api/returns"),

    (ai_assistant_bp, "/api/ai-assistants"),
    (ai_draft_order_bp, "/api/ai-draft-orders"),
]


def register_routes(app):
    for blueprint, prefix in ROUTE_GROUPS:
        app.register_blueprint(blueprint, url_prefix=prefix)

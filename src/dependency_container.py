from dependency_injector import containers, providers
from infrastructure.databases import session 

# --- 1. REPOSITORIES ---
# Access & Identity
from infrastructure.repositories.access_and_identity_repo.administrator_repository import AdministratorRepository
from infrastructure.repositories.access_and_identity_repo.business_owner_repository import BusinessOwnerRepository
from infrastructure.repositories.access_and_identity_repo.employee_repository import EmployeeRepository
from infrastructure.repositories.access_and_identity_repo.subscription_plan_repository import SubscriptionPlanRepository

# Inventory
from infrastructure.repositories.inventory_repo.product_repository import ProductRepository
from infrastructure.repositories.inventory_repo.unit_repository import UnitRepository
from infrastructure.repositories.inventory_repo.supplier_repository import SupplierRepository
from infrastructure.repositories.inventory_repo.stock_import_repository import StockImportRepository
from infrastructure.repositories.inventory_repo.stock_import_detail_repository import StockImportDetailRepository
from infrastructure.repositories.inventory_repo.category_repository import CategoryRepository
from infrastructure.repositories.inventory_repo.inventory_check_repository import InventoryCheckRepository

# Sale & Finance
from infrastructure.repositories.sale_and_finance_repo.customer_repository import CustomerRepository
from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.order_detail_repository import OrderDetailRepository
from infrastructure.repositories.sale_and_finance_repo.payment_repository import PaymentRepository
from infrastructure.repositories.sale_and_finance_repo.debt_repository import DebtRepository
from infrastructure.repositories.sale_and_finance_repo.return_order_repository import ReturnOrderRepository
from infrastructure.repositories.sale_and_finance_repo.expense_repository import ExpenseRepository
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository

# AI Core
from infrastructure.repositories.ai_core_repo.ai_assistant_repository import AIAssistantRepository
from infrastructure.repositories.ai_core_repo.ai_draft_order_repository import AIDraftOrderRepository

# --- 2. SERVICES ---
from services.auth_service import AuthService
from services.access_and_identity_service.administrator_service import AdministratorService
from services.access_and_identity_service.business_owner_service import BusinessOwnerService
from services.access_and_identity_service.employee_service import EmployeeService
from services.access_and_identity_service.subscription_plan_service import SubscriptionPlanService

from services.inventory_service.product_service import ProductService
from services.inventory_service.unit_service import UnitService
from services.inventory_service.supplier_service import SupplierService
from services.inventory_service.stock_import_service import StockImportService
from services.inventory_service.stock_import_detail_service import StockImportDetailService
from services.inventory_service.category_service import CategoryService
from services.inventory_service.inventory_check_service import InventoryCheckService

from services.sale_and_finance_service.customer_service import CustomerService
from services.sale_and_finance_service.order_service import OrderService
from services.sale_and_finance_service.order_detail_service import OrderDetailService
from services.sale_and_finance_service.payment_service import PaymentService
from services.sale_and_finance_service.debt_service import DebtService
from services.sale_and_finance_service.return_order_service import ReturnOrderService
from services.sale_and_finance_service.expense_service import ExpenseService
from services.sale_and_finance_service.account_report_service import AccountReportService

from services.ai_sore_service.ai_assistant_service import AIAssistantService
from services.ai_sore_service.ai_draft_order_service import AIDraftOrderService





class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=[
        "api.controllers.auth_controller",
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.access_and_identity_control.subscription_plan_controller",
        "api.controllers.inventory_control.product_controller",
        "api.controllers.inventory_control.unit_controller",
        "api.controllers.inventory_control.supplier_controller",
        "api.controllers.inventory_control.stock_import_controller",
        "api.controllers.inventory_control.stock_import_detail_controller",
        "api.controllers.inventory_control.category_controller",
        "api.controllers.inventory_control.inventory_check_controller", # ✅ Đã thêm
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.sale_and_finance_control.order_detail_controller",
        "api.controllers.sale_and_finance_control.payment_controller",
        "api.controllers.sale_and_finance_control.debt_controller",
        "api.controllers.sale_and_finance_control.return_order_controller", # ✅ Đã thêm
        "api.controllers.sale_and_finance_control.expense_controller",      # ✅ Đã thêm
        "api.controllers.sale_and_finance_control.account_report_controller",
        "api.controllers.ai_core_control.ai_assistant_controller",
        "api.controllers.ai_core_control.ai_draft_order_controller",
        
    ])

    # Fix lỗi deepcopy session
    db_session = providers.Object(session)

    # --- REPOSITORIES ---
    admin_repo = providers.Factory(AdministratorRepository, session=db_session)
    business_owner_repo = providers.Factory(BusinessOwnerRepository, session=db_session)
    employee_repo = providers.Factory(EmployeeRepository, session=db_session)
    subscription_plan_repo = providers.Factory(SubscriptionPlanRepository, session=db_session)

    product_repo = providers.Factory(ProductRepository, session=db_session)
    unit_repo = providers.Factory(UnitRepository, session=db_session)
    supplier_repo = providers.Factory(SupplierRepository, session=db_session)
    stock_import_repo = providers.Factory(StockImportRepository, session=db_session)
    stock_import_detail_repo = providers.Factory(StockImportDetailRepository, session=db_session)
    category_repo = providers.Factory(CategoryRepository, session=db_session)
    inventory_check_repo = providers.Factory(InventoryCheckRepository, session=db_session)

    customer_repo = providers.Factory(CustomerRepository, session=db_session)
    order_repo = providers.Factory(OrderRepository, session=db_session)
    order_detail_repo = providers.Factory(OrderDetailRepository, session=db_session)
    payment_repo = providers.Factory(PaymentRepository, session=db_session)
    debt_repo = providers.Factory(DebtRepository, session=db_session)
    return_order_repo = providers.Factory(ReturnOrderRepository, session=db_session)
    expense_repo = providers.Factory(ExpenseRepository, session=db_session)
    account_report_repository = providers.Factory(
        AccountReportRepository
    )


    ai_assistant_repo = providers.Factory(AIAssistantRepository, session=db_session)
    ai_draft_order_repo = providers.Factory(AIDraftOrderRepository, session=db_session)
    

    # --- SERVICES ---
    auth_service = providers.Factory(
        AuthService, 
        admin_repo=admin_repo, 
        business_owner_repo=business_owner_repo, 
        employee_repo=employee_repo
    )
    
    administrator_service = providers.Factory(AdministratorService, repository=admin_repo)
    business_owner_service = providers.Factory(BusinessOwnerService, repository=business_owner_repo)
    employee_service = providers.Factory(EmployeeService, repository=employee_repo)
    subscription_plan_service = providers.Factory(SubscriptionPlanService, repository=subscription_plan_repo)

    product_service = providers.Factory(ProductService, repository=product_repo)
    unit_service = providers.Factory(UnitService, repository=unit_repo)
    supplier_service = providers.Factory(SupplierService, repository=supplier_repo)
    stock_import_service = providers.Factory(StockImportService, repository=stock_import_repo)
    stock_import_detail_service = providers.Factory(StockImportDetailService, repository=stock_import_detail_repo)
    category_service = providers.Factory(CategoryService, repository=category_repo)
    
    # Inventory Check cần product_repo để cập nhật kho
    inventory_check_service = providers.Factory(
        InventoryCheckService, 
        repository=inventory_check_repo,
        product_repository=product_repo # ✅ Chuẩn
    )

    debt_service = providers.Factory(DebtService, repository=debt_repo)
    customer_service = providers.Factory(CustomerService, repository=customer_repo)
    
    order_service = providers.Factory(
        OrderService, 
        repository=order_repo, 
        product_repo=product_repo,
        debt_service=debt_service
    )
    
    order_detail_service = providers.Factory(OrderDetailService, repository=order_detail_repo)
    payment_service = providers.Factory(PaymentService, repository=payment_repo)
    
    # Return Order cần product_repo để cộng lại kho
    return_order_service = providers.Factory(
        ReturnOrderService, 
        repository=return_order_repo,
        product_repo=product_repo  # 👈 BẮT BUỘC PHẢI CÓ DÒNG NÀY
    )

    expense_service = providers.Factory(ExpenseService, repository=expense_repo)
    

    ai_assistant_service = providers.Factory(AIAssistantService, repository=ai_assistant_repo)
    ai_draft_order_service = providers.Factory(
        AIDraftOrderService, 
        repository=ai_draft_order_repo,
        order_service=order_service,
        product_service=product_service,
        customer_service=customer_service
    )
    report_service = providers.Factory(
        AccountReportService,
        repository=account_report_repository
    )
from dependency_injector import containers, providers
from infrastructure.databases import session 
from config import Config
# ==========================================================
# 1. IMPORT REPOSITORIES
# ==========================================================

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



# ==========================================================
# 2. IMPORT SERVICES
# ==========================================================
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
    db_session_provider = providers.Object(session)
    # 🛠️ CẤU HÌNH WIRING (Đây là chỗ bạn bị thiếu, mình đã điền đủ 100%)
    wiring_config = containers.WiringConfiguration(modules=[
        # Auth
        "api.controllers.auth_controller",
        
        # Access & Identity (QUAN TRỌNG: 2 file này đã được thêm vào)
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.access_and_identity_control.subscription_plan_controller",
        
        # Inventory
        "api.controllers.inventory_control.category_controller",
        "api.controllers.inventory_control.product_controller",
        "api.controllers.inventory_control.unit_controller",
        "api.controllers.inventory_control.supplier_controller",
        "api.controllers.inventory_control.stock_import_controller",
        "api.controllers.inventory_control.stock_import_detail_controller",
        "api.controllers.inventory_control.inventory_check_controller",
        
        # Sale & Finance
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.sale_and_finance_control.order_detail_controller",
        "api.controllers.sale_and_finance_control.payment_controller",
        "api.controllers.sale_and_finance_control.debt_controller",
        "api.controllers.sale_and_finance_control.return_order_controller",
        "api.controllers.sale_and_finance_control.expense_controller",
        "api.controllers.sale_and_finance_control.account_report_controller",
        
        # AI Core
        "api.controllers.ai_core_control.ai_assistant_controller",
        "api.controllers.ai_core_control.ai_draft_order_controller",

       
    ])

    # Fix lỗi deepcopy session
    db_session = providers.Object(session)

    # ==========================================================
    # 3. REGISTER REPOSITORIES
    # ==========================================================
    
    subscription_plan_repository = providers.Factory(
        SubscriptionPlanRepository, 
        session=db_session_provider # Giữ là 'session' nếu repo này dùng tên đó
    )

    business_owner_repository = providers.Factory(
        BusinessOwnerRepository,
        session=db_session_provider # Giữ là 'session' vì BusinessOwnerRepository dùng 'session'
    )

    administrator_repository = providers.Factory(
        AdministratorRepository,
        db_session=db_session_provider # Dùng 'db_session'
    )

    employee_repository = providers.Factory(
        EmployeeRepository,
        db_session=db_session_provider # Dùng 'db_session'
    )

    # Inventory - SỬA LẠI TẤT CẢ THÀNH 'db_session' CHO KHỚP VỚI REPO
    product_repository = providers.Factory(
        ProductRepository, 
        db_session=db_session_provider # Đã sửa từ 'session' thành 'db_session'
    )
    
    unit_repository = providers.Factory(UnitRepository, db_session=db_session_provider)
    supplier_repository = providers.Factory(SupplierRepository, db_session=db_session_provider)
    stock_import_repository = providers.Factory(StockImportRepository, db_session=db_session_provider)
    stock_import_detail_repository = providers.Factory(StockImportDetailRepository, db_session=db_session_provider)
    category_repository = providers.Factory(CategoryRepository, db_session=db_session_provider)
    inventory_check_repository = providers.Factory(InventoryCheckRepository, db_session=db_session_provider)

    # Sale & Finance
    customer_repository = providers.Factory(CustomerRepository, db_session=db_session_provider)
    
    order_repository = providers.Factory(
        OrderRepository, 
        db_session=db_session_provider # Đã sửa từ 'session' thành 'db_session'
    )
    
    order_detail_repository = providers.Factory(OrderDetailRepository, db_session=db_session_provider)
    payment_repository = providers.Factory(PaymentRepository, db_session=db_session_provider)
    debt_repository = providers.Factory(DebtRepository, db_session=db_session_provider)
    return_order_repository = providers.Factory(ReturnOrderRepository, db_session=db_session_provider)
    expense_repository = providers.Factory(ExpenseRepository, db_session=db_session_provider)
    account_report_repository = providers.Factory(AccountReportRepository, db_session=db_session_provider)

    # AI & Todo
    ai_assistant_repository = providers.Factory(AIAssistantRepository, db_session=db_session_provider)
    ai_draft_order_repository = providers.Factory(AIDraftOrderRepository, db_session=db_session_provider)
    # ==========================================================
    # 4. REGISTER SERVICES
    # ==========================================================

    # --- 1. CORE SERVICES (Độc lập) ---
    administrator_service = providers.Factory(
        AdministratorService, 
        repository=administrator_repository # Đã đổi từ admin_repo thành administrator_repo
    )
    auth_service = providers.Factory(
        AuthService,
        admin_repo=administrator_repository,
        owner_repo=business_owner_repository,
        employee_repo=employee_repository,
        secret_key=Config.SECRET_KEY # Truyền key từ file config vào đây
    )

    
    business_owner_service = providers.Factory(BusinessOwnerService, repository=business_owner_repository)
    employee_service = providers.Factory(EmployeeService, repository=employee_repository)
    subscription_plan_service = providers.Factory(SubscriptionPlanService, repository=subscription_plan_repository)

    product_service = providers.Factory(ProductService, repository=product_repository)
    unit_service = providers.Factory(UnitService, repository=unit_repository)
    supplier_service = providers.Factory(SupplierService, repository=supplier_repository)
    stock_import_service = providers.Factory(StockImportService, repository=stock_import_repository)
    stock_import_detail_service = providers.Factory(StockImportDetailService, repository=stock_import_detail_repository)
    category_service = providers.Factory(CategoryService, repository=category_repository)
    
    # Inventory Check (Cần product_repo để trừ kho)
    inventory_check_service = providers.Factory(
        InventoryCheckService, 
        repository=inventory_check_repository,
        product_repository=product_repository
    )

    # --- 2. DEPENDENT SERVICES (Có phụ thuộc) ---
    debt_service = providers.Factory(DebtService, repository=debt_repository)

    # Đưa Customer Service lên đây để AI dùng
    customer_service = providers.Factory(CustomerService, repository=customer_repository)

    order_service = providers.Factory(
        OrderService, 
        repository=order_repository,
        product_repo=product_repository,
        debt_service=debt_service
    )
    
    order_detail_service = providers.Factory(OrderDetailService, repository=order_detail_repository)
    payment_service = providers.Factory(PaymentService, repository=payment_repository)
    
    # Return Order (Cần product_repo để cộng kho)
    return_order_service = providers.Factory(
        ReturnOrderService, 
        repository=return_order_repository,
        product_repo=product_repository
    )
    
    expense_service = providers.Factory(ExpenseService, repository=expense_repository)
    account_report_service = providers.Factory(AccountReportService, repository=account_report_repository)

    # --- 3. AI SERVICES ---
    ai_assistant_service = providers.Factory(AIAssistantService, repository=ai_assistant_repository)
    
    ai_draft_order_service = providers.Factory(
        AIDraftOrderService, 
        repository=ai_draft_order_repository,
        order_service=order_service,
        product_service=product_service,
        customer_service=customer_service 
    )

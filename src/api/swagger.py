from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.todo import TodoRequestSchema, TodoResponseSchema

spec = APISpec(
    title="Bizflow",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Đăng ký schema để tự động sinh model
spec.components.schema("TodoRequest", schema=TodoRequestSchema)
spec.components.schema("TodoResponse", schema=TodoResponseSchema)

from api.schemas.business_owner import BusinessOwnerRequestSchema, BusinessOwnerResponseSchema

spec.components.schema("BusinessOwnerRequest", schema=BusinessOwnerRequestSchema)
spec.components.schema("BusinessOwnerResponse", schema=BusinessOwnerResponseSchema)


from api.schemas.administrator import AdministratorRequestSchema, AdministratorResponseSchema

# Thêm vào đoạn cuối file swagger.py
spec.components.schema("AdministratorRequest", schema=AdministratorRequestSchema)
spec.components.schema("AdministratorResponse", schema=AdministratorResponseSchema)

from api.schemas.employee import EmployeeRequestSchema, EmployeeResponseSchema

spec.components.schema("EmployeeRequest", schema=EmployeeRequestSchema)
spec.components.schema("EmployeeResponse", schema=EmployeeResponseSchema)


from api.schemas.product import ProductRequestSchema, ProductResponseSchema

spec.components.schema("ProductRequest", schema=ProductRequestSchema)
spec.components.schema("ProductResponse", schema=ProductResponseSchema)

from api.schemas.subscription_plan import SubscriptionPlanRequestSchema, SubscriptionPlanResponseSchema
spec.components.schema("SubscriptionPlanRequest", schema=SubscriptionPlanRequestSchema)
spec.components.schema("SubscriptionPlanResponse", schema=SubscriptionPlanResponseSchema)


from api.schemas.customer import CustomerRequestSchema, CustomerResponseSchema

spec.components.schema("CustomerRequest", schema=CustomerRequestSchema)
spec.components.schema("CustomerResponse", schema=CustomerResponseSchema)


from api.schemas.unit import UnitRequestSchema, UnitResponseSchema

spec.components.schema("UnitRequest", schema=UnitRequestSchema)
spec.components.schema("UnitResponse", schema=UnitResponseSchema)

from api.schemas.order import OrderRequestSchema, OrderResponseSchema

spec.components.schema("OrderRequest", schema=OrderRequestSchema)
spec.components.schema("OrderResponse", schema=OrderResponseSchema)

from api.schemas.order_detail import OrderDetailRequestSchema, OrderDetailResponseSchema

spec.components.schema("OrderDetailRequest", schema=OrderDetailRequestSchema)
spec.components.schema("OrderDetailResponse", schema=OrderDetailResponseSchema)

from api.schemas.debt import DebtRequestSchema, DebtResponseSchema

spec.components.schema("DebtRequest", schema=DebtRequestSchema)
spec.components.schema("DebtResponse", schema=DebtResponseSchema)

from api.schemas.payment import PaymentRequestSchema, PaymentResponseSchema

spec.components.schema("PaymentRequest", schema=PaymentRequestSchema)
spec.components.schema("PaymentResponse", schema=PaymentResponseSchema)

from api.schemas.account_report import AccountReportRequestSchema, AccountReportResponseSchema

spec.components.schema("AccountReportRequest", schema=AccountReportRequestSchema)
spec.components.schema("AccountReportResponse", schema=AccountReportResponseSchema)

from api.schemas.ai_assistant import AIAssistantRequestSchema, AIAssistantResponseSchema
spec.components.schema("AIAssistantRequest", schema=AIAssistantRequestSchema)
spec.components.schema("AIAssistantResponse", schema=AIAssistantResponseSchema)


from api.schemas.ai_draft_order import AIDraftOrderRequestSchema, AIDraftOrderResponseSchema
spec.components.schema("AIDraftOrderRequest", schema=AIDraftOrderRequestSchema)
spec.components.schema("AIDraftOrderResponse", schema=AIDraftOrderResponseSchema)








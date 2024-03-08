from ninja import Router

from core.api.v1.customers.handlers import router as customer_router
from core.api.v1.products.handlers import product_router


router = Router()
router.add_router('products/', product_router)
router.add_router('customer/', customer_router)

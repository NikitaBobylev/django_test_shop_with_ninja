from ninja import Router

from core.api.v1.products.handlers import product_router


router = Router()
router.add_router('products/', product_router)

from api.views import ProductView, OrderView
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('product', ProductView)
router.register('order', OrderView)


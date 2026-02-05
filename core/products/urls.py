from django.urls import path, include
from products.views import ProductsView, CategoriesView, SellerView, WarehouseView, CurrencyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductsView, basename='products')
router.register(r'categories', CategoriesView, basename='categories')
router.register(r'sellers', SellerView, basename='sellers')
router.register(r'warehouse', WarehouseView, basename='warehouse')
router.register(r'currency', CurrencyView, basename='currency')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from products.views import ProductsView, CategoriesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productslist', ProductsView, basename='products_list')
router.register(r'categories', CategoriesView, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]
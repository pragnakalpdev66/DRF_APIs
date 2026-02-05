import urllib.request as url_request
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from products.serializers import ProductsSerializer, CategoriesSerializer, SellerSerializer, WarehouseSerializer, CurrencySerializer, BuyProductSerializer
from products.models import Products, Categories, Person, Warehouse, Currency
from products.paginations import ProductPagination
from products.filters import ProductFilter
from authentication.permissions import IsAdminOrReadOnly, IsRegularUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.throttling import ScopedRateThrottle
from products.throttles import BuyProductThrottle

@method_decorator(cache_page(60 * 15), name='list')
@method_decorator(cache_page(60 * 15), name='retrieve')
class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Products.objects.all().filter(is_deleted=False)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)   
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_deleted = True
        product.is_available = False
        product.stock = 0
        print("is_available: ", product.is_available)
        product.save()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsRegularUser], throttle_classes = [BuyProductThrottle])
    def buy(self, request, pk=None):
        product = self.get_object()

        serializer = BuyProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data['quantity']

        # if not request.user or not request.user.is_authenticated:
        #     return Response(
        #         {"message": "Please login first !!"}, 
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )
        
        # if request.user.is_staff:
        #     return Response(
        #         {"message": "Please use Regular/User Account !!"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        
        if not product.is_available:
            print("prodcut's availability: ",product.is_available)
            return Response(
                {"message": "Product is not available !!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if product.stock < quantity:
            print("at quantity check,\nproduct-quentity: ",quantity, "\nstock: ",product.stock)
            return Response(
                {"message": "low stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.stock -= quantity
        print("product-quantity: ",quantity, "\nstock: ",product.stock)
        if product.stock == 0:
            product.is_available = False
        product.save()

        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_updates",
            {
                "type": "send_notification",
                "message": {
                    "event": "ORDER PLACED",
                    "product_name": product.product_name,
                    "buyer": request.user.first_name,
                    "quantity": request.data.get('quantity', 1)
                }
            }
        )
        # response in postman
        return Response(
            {
                "message": "Product purchased successfully",
                "product_id": product.id,
                "product_name": product.product_name,
                # "product": ProductsSerializer(product, context={"request": request}).data,
                "quantity": quantity,
                "remaining_stock": product.stock
            },
            status=status.HTTP_200_OK
        )

    
class CategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_class = ProductFilter

    filterset_fields = ['category_name']
    search_fields = ['category_name']
    ordering_fields = ['-created_at']

    def get_queryset(self):
        return Categories.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        print("enter for destroy")
        category = self.get_object()
        category.is_deleted = True
        category.save()
        print(f"deleted {category}")
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)

class SellerView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAdminOrReadOnly]

class WarehouseView(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes =[IsAdminOrReadOnly]

class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAdminOrReadOnly]
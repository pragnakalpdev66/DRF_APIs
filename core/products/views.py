from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from products.serializers import ProductsSerializer, CategoriesSerializer
from products.models import Products, Categories
from products.paginations import ProductPagination
from products.filters import ProductFilter
from authentication.permissions import IsAdminOrReadOnly

class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter

    # filterset_fields = ['category__category_name', 'brand_name', 'currency', 'is_available']
    # search_fields = ['product_name', 'brand_name']
    # ordering_fields = ['price', 'created_at']
    # ordering = ['-created_at']

    def get_queryset(self):
        queryset = Products.objects.all().filter(is_deleted=False)
        # queryset.filter(is_deleted=False)
                # print("displaying list: ", queryset)
        # queryset = ProductFilter.apply_product_filters(queryset, self.request.query_params)
        # queryset.order_by('-created_at')

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    # def partial_update(self, request, *args, **kwargs):
    #     response = super().partial_update(request, *args, **kwargs)

    #     if response.status_code == status.HTTP_200_OK:
    #         print("updated partially")
    #     else: 
    #         print("partial updated not successfull!!")

    #     return response
        
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_deleted = True
        product.is_available = False
        product.stock = 0
        print("is_available: ", product.is_available)
        product.save()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)

class CategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]

    filterset_fields = ['category_name']
    search_fields = ['category_name']
    ordering_fields = ['-created_at']

    def get_queryset(self):
        return Categories.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.is_deleted = True
        category.save()
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)

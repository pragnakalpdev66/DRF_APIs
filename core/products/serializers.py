import json
from rest_framework import serializers
from products.models import Products, Person, Categories, Warehouse, Currency
from django.utils.text import slugify
import random, string
        
def generate_unique_slug(name):

    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while Products.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug
    
class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']

class ProductsSerializer(serializers.ModelSerializer):

    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), source='category', write_only=True, required=False)

    # created_by = serializers.ReadOnlyField(source='created_by.firstname')
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)
    print("created_by: ", created_by)

    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), many=True, required=False)
    product_image = serializers.ImageField(required=False, allow_null=True)
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), source='seller', write_only=True, required=False)

    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), source='currency', write_only=True)
    
    class Meta:
        model = Products
        fields = "__all__"
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'is_deleted']
    
    # def get_product_image(self, obj):
    #     if not obj.product_image:
    #         return None
        
    #     request = self.context.get('request')
    #     file_url = obj.product_image.url        
    #     custom_path = f"/api/v1{file_url}"
        
    #     if request is not None:
    #         return request.build_absolute_uri(custom_path)
            
    #     return custom_path
    
    def get_product_image(self, obj):
        if not obj.product_image:
            return None

        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.product_image.url)

        return obj.product_image.url
    
    def to_representation(self, instance):
        # print("Raw Data1:", data)
        data = super().to_representation(instance)
        print("Raw Data2:", data)
        # product_img = data.pop('product_image', None)
        # data['image'] = product_img if product_img is not None else data.get('image')
        data['image'] = data.pop('product_image', None) or data.get('image')

        data['name'] = data.pop('product_name', None) or data.get('name')

        # data['isRefurnished'] = data.pop('is_refurnished', None) or data.get('isRefurnished')
        data['isRefurnished'] = data.pop('is_refurnished', None)

        data['skuCode'] = data.pop('sku', None) or data.get('skuCode')
        data['brand'] = data.pop('brand_name', None) or data.get('brand')
        data['isAvailable'] = data.pop('is_available', None) or data.get('isAvailable')

        warehouses_qs = instance.warehouse.all() 
        data['stockWareHouseList'] = WarehouseSerializer(warehouses_qs, many=True).data
        data.pop('warehouse', None) or data.get('stockWareHouseList')
        data['stockWareHouseList'] = data.pop('warehouse', None) or data.get('stockWareHouseList')
        
        return data
    
    def to_internal_value(self, data):

        if hasattr(data, 'dict'):
            data = data.dict()
        else:
            data = data.copy()

        mappings = {
            'image': 'product_image',
            'name': 'product_name',
            'brand': 'brand_name',
            'isAvailable': 'is_available',
            'isRefurnished': 'is_refurnished',
            'skuCode': 'sku',
            'stockWareHouseList': 'warehouse',
            'currency': 'currency_id',
            'category': 'category_id',
            'seller': 'seller_id',
        }

        for f_key, b_key in mappings.items():
            if f_key in data and b_key not in data:
                data[b_key] = data.pop(f_key)

        # if 'warehouse' in data:
        #     val = data['warehouse']
        #     if isinstance(val, str):
        #         data['warehouse'] = [id.strip() for id in val.split(',') if id.strip()]
            
        #     if val == "" or val is None:
        #         data['warehouse'] = []
        

        if 'warehouse' in data:
            val = data['warehouse']
            
            if isinstance(val, str) and val.startswith('['):
                try:
                    data['warehouse'] = json.loads(val)
                except (ValueError, TypeError):
                    data['warehouse'] = []
            
            elif isinstance(val, str):
                data['warehouse'] = [id.strip() for id in val.split(',') if id.strip()]
            
            if not data['warehouse']:
                data['warehouse'] = []

        return super().to_internal_value(data)

    def create(self, validated_data):
        product_name = validated_data['product_name']
        validated_data['slug'] = generate_unique_slug(product_name)

        warehouses = validated_data.pop('warehouse', [])
        product = super().create(validated_data)
        if warehouses:
            product.warehouse.set(warehouses)
        # print("created_by: ", self.created_by)
        # return super().create(validated_data) 
        print("product: ", product)
        return product

    def update(self, instance, validated_data):
        if "product_name" in validated_data:
            new_name = validated_data["product_name"]
            if new_name != instance.product_name:
                validated_data["slug"] = generate_unique_slug(new_name)

        warehouses = validated_data.pop('warehouse', None)

        instance = super().update(instance, validated_data)

        if warehouses is not None:
            instance.warehouse.set(warehouses)

        return instance
    
    def validate_warehouse(self, value):
        # if isinstance(value, list) and len(value) > 0 and isinstance(value[0], str):
        #     warehouses = Warehouse.objects.filter(id__in=value)
            
        #     if warehouses.count() != len(value):
        #         raise serializers.ValidationError("Invalid warehouse ID(s) provided.")
            
        #     return list(warehouses) 
        if isinstance(value, str):
            value = [value]
            
        return value


class BuyProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
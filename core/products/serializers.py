from rest_framework import serializers
from products.models import Products, Person, Categories
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

class ProductsSerializer(serializers.ModelSerializer):

    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), source='category', write_only=True, required=False)
    created_by = serializers.ReadOnlyField(source='created_by.firstname')
    print("created_by: ", created_by)
    
    class Meta:
        model = Products
        fields = "__all__"
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'is_deleted']

    def create(self, validated_data):
        product_name = validated_data['product_name']
        
        validated_data['slug'] = generate_unique_slug(product_name)
        # print("created_by: ", self.created_by)
        return super().create(validated_data) 

    def update(self, instance, validated_data):
        if "product_name" in validated_data:
            new_name = validated_data["product_name"]
            if new_name != instance.product_name:
                validated_data["slug"] = generate_unique_slug(new_name)

        return super().update(instance, validated_data)
    
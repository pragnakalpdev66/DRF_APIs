from django.db import models
from authentication.models import User, TrackFields
from django.core.validators import MinValueValidator
import uuid

CURRNENCY_CHOICES = [
        ('USD','US Dollar'),
        ('INR', 'Rupee'),
        ('EUR', 'Euro'),
        ('CAD', 'Canadian Dollar')
    ]

FIELDS_NAME = {
    "category":"category__category_name",
    "seller":"seller__seller_name",
    "created_by":"created_by__first_name"
}



class Person(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    seller_name = models.CharField(max_length=20)

    class Meta:
        app_label = 'products'
    
    def __str__(self):
        return f"{self.seller_name}"


class Categories(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    category_name = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = 'products'

    def __str__(self):
        return f"{self.category_name}"

class Products(TrackFields):
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)

    product_name = models.CharField(max_length=50)
    description = models.TextField(default=None)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    brand_name = models.CharField(max_length=20)
    slug = models.CharField(max_length=200, unique=True)
    sku = models.CharField(max_length=200,unique=True, blank=True) # len 12         ##
    currency = models.CharField(max_length=3, choices=CURRNENCY_CHOICES)
    price = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=False)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)] )
    product_image = models.ImageField(upload_to='media/products/', blank=True)
    seller = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'products'
        
    def __str__(self):
        return f"{self.product_name} in {self.category}"
    

    def get_column_name(field_name: str) -> str:
        string = FIELDS_NAME.get(field_name,field_name)
        return string

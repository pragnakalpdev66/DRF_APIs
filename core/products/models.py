from django.db import models
from authentication.models import User, TrackFields
from django.core.validators import MinValueValidator
import uuid
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

FIELDS_NAME = {
    "category":"category__category_name",
    "seller":"seller__seller_name",
    "created_by":"created_by__first_name"
}

def validate_image_size(image):
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image file too large!! Size should not exceed 2MB.")


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
    
class Currency(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    currency = models.CharField(unique=True)

    class Meta:
        app_label = 'products'

    def __str__(self):
        return f"{self.currency}"

class Warehouse(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    warehouse_city = models.CharField(max_length=100)
    pincode = models.IntegerField(max_length=6)

    class Meta:
        app_label = 'products'
    
    def __str__(self):
        return f"{self.warehouse_city}"

class Products(TrackFields):
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)

    product_name = models.CharField(max_length=50)
    description = models.TextField(default=None)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    brand_name = models.CharField(max_length=20)
    slug = models.CharField(max_length=200, unique=True)
    sku_regex = RegexValidator(
        regex=r'^[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{4}$',
        message="SKU must be in the format 'AB0-C23-2BCD' (exactly 12 characters)."
    )
    sku = models.CharField(max_length=12,unique=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=False)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)] )
    product_image = models.ImageField(upload_to='media/products/', blank=True, validators=[validate_image_size] )
    seller = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_refurnished = models.BooleanField(default=False)
    warehouse = models.ManyToManyField(Warehouse)

    class Meta:
        app_label = 'products'
        
    def __str__(self):
        return f"{self.product_name} in {self.category}"
    
    def get_column_name(field_name: str) -> str:
        string = FIELDS_NAME.get(field_name,field_name)
        return string
    
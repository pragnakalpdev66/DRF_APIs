from django.db import models
from authentication.models import User, TrackFields
import uuid

FIELDS_NAME = {
    "author": "author__first_name",
    "genre": "genre__genre_name",
    "publisher": "publisher__name",
    "language": "language",
}

SORTED_VALUES = {
    "latest": "-created_at",
    "old": "created_at",
    "a-z": "book_title",
    "z-a": "-book_title",
    "newest_publish": "-published_date",
    "oldest_publish": "published_date",
}

class Author(TrackFields):
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(default=None)
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        app_label = 'books'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Publisher(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    website = models.URLField(max_length=200)
    country = models.CharField(max_length=20)

    class Meta:
        app_label = 'books'

    def __str__(self):
        return f"publisher: {self.name}"
    
class Genre(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    genre_name = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = 'books'
        
    def __str__(self):
        return f"{self.genre_name}"
    
class Books(TrackFields):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    book_title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=20)
    isbn = models.IntegerField('ISBN', max_length=13, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    published_date = models.DateField(blank=True, null=True)
    description = models.TextField(default=None)
    is_avialable = models.BooleanField(default=True)
    book_image = models.ImageField(upload_to='media/books/', blank=True)

    class Meta:
        app_label = 'books'
        
    def __str__(self):
        return f"{self.book_title} by {self.author}"
    
    def get_column_name(field_name: str) -> str:
        return FIELDS_NAME.get(field_name, field_name)

    def get_sorted_values(sorted_value: str) -> str:
        return SORTED_VALUES.get(sorted_value)

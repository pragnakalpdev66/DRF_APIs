from django.contrib import admin

from books.models import Books, Author, Genre, Publisher

admin.site.register(Books)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Publisher)
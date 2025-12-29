from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BooksViewSet, AuthorViewSet, GenreViewSet, PublisherViewSet

router = DefaultRouter()
router.register(r'book', BooksViewSet, basename='book')
router.register(r'author', AuthorViewSet, basename='author')
router.register(r'genre', GenreViewSet, basename='genre')
router.register(r'publisher', PublisherViewSet, basename='publisher')

urlpatterns = [
    path('', include(router.urls)),
]

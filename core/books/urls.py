from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BooksViewSet, AuthorViewSet, GenreViewSet, PublisherViewSet

router = DefaultRouter()
router.register(r'books', BooksViewSet, basename='books')
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'publishers', PublisherViewSet, basename='publishers')

urlpatterns = [
    path('', include(router.urls)),
]

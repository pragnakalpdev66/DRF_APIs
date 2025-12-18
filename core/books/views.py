from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from books.models import Books, Author, Genre, Publisher
from books.serializers import BooksSerializer, AuthorSerializer, GenreSerializer, PublisherSerializer
from books.filters import BookFilter
from books.pagination import BookPagination
from authentication.permissions import IsAdminOrReadOnly


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = BooksSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = Books.objects.filter(is_deleted=False)
        print("Books count:", queryset.count())
        return queryset

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.is_deleted = True
        book.save()
        print("Book soft deleted:", book.book_title)
        return Response({"message": "Book deleted"}, status=status.HTTP_204_NO_CONTENT)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.filter(is_deleted=False)
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        author.is_deleted = True
        author.save()
        print("Author soft deleted:", author.first_name, author.last_name)
        return Response(
            {"message": "Author deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.filter(is_deleted=False)
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        genre = self.get_object()
        genre.is_deleted = True
        genre.save()
        print("Genre soft deleted:", genre.genre_name)
        return Response(
            {"message": "Genre deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.filter(is_deleted=False)
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        publisher = self.get_object()
        publisher.is_deleted = True
        publisher.save()
        print("Publisher soft deleted:", publisher.name)
        return Response(
            {"message": "Publisher deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


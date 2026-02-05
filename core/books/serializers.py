from rest_framework import serializers
from books.models import Books, Author, Genre, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']


class BooksSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    author_id = serializers.UUIDField(write_only=True, required=True)
    genre_id = serializers.UUIDField(write_only=True, required=True)
    publisher_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = Books
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted']

    def create(self, validated_data):
        print("Creating Book:", validated_data.get("book_title"))

        author_id = validated_data.pop("author_id")
        genre_id = validated_data.pop("genre_id")
        publisher_id = validated_data.pop("publisher_id")

        validated_data["author"] = Author.objects.get(id=author_id)
        validated_data["genre"] = Genre.objects.get(id=genre_id)
        validated_data["publisher"] = Publisher.objects.get(id=publisher_id)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        print("Updating Book:", instance.book_title)

        if "author_id" in validated_data:
            instance.author = Author.objects.get(id=validated_data.pop("author_id"))

        if "genre_id" in validated_data:
            instance.genre = Genre.objects.get(id=validated_data.pop("genre_id"))

        if "publisher_id" in validated_data:
            instance.publisher = Publisher.objects.get(id=validated_data.pop("publisher_id"))

        return super().update(instance, validated_data)


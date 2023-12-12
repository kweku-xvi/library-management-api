from .models import Book, CheckoutBook
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'cover_image', 'description', 'authors', 'genre', 'date_published', 'publisher', 'number_of_pages', 'language', 'checked_out']


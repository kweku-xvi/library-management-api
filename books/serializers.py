from .models import Book, CheckoutBook
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'cover_image', 'description', 'authors', 'genre', 'date_published', 'publisher', 'number_of_pages', 'language', 'checked_out']


# class CheckoutBookSerializer(serializers.ModelSerializer):
#     book = serializers.SerializerMethodField()
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = CheckoutBook
#         fields = ['id', 'book', 'user', 'due_date']

#     def get_book(self, obj):
#         return obj.book.title if obj.book else None

#     def get_user(self, obj):
#         return obj.user.username if obj.user else None
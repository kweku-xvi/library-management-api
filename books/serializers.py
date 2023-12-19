from .models import Book, CheckoutBook, ReserveBook
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'cover_image', 'description', 'authors', 'genre', 'date_published', 'publisher', 'number_of_pages', 'language', 'available', 'shelf_location']


class ReservesSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = ReserveBook
        fields = ['reservation_id', 'book']

    def get_book(self, obj):
        return obj.book.title if obj.book else None


class CheckoutSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = CheckoutBook
        fields = ['checkout_id', 'user', 'book', 'borrow_date', 'due_date']

    def get_book(self, obj):
        return obj.book.title if obj.book else None 

    def get_user(self, obj):
        return obj.user.username if obj.user else None
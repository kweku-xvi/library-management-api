from .models import Book, CheckoutBook
from .serializers import BookSerializer
from accounts.permissions import IsVerified
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


def get_book(isbn:str):
    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return Response(
            {
                'success':True,
                'message':'Book does not exist!'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return book

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_books_view(request):
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':'Book has been added!',
                    'book':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_book_details_view(request, isbn:str):
    if request.method == 'GET':
        book = get_book(isbn=isbn)

        serializer = BookSerializer(book)

        return Response(
            {
                'success':True,
                'book':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_all_books_view(request):
    if request.method == 'GET':
        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'books':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_book_details_view(request, isbn:str):
    if request.method == 'PUT' or request.method == 'PATCH':
        book = get_book(isbn=isbn)

        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':'Book details has been successfully updated!',
                    'book':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':True,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book_view(request, isbn:str):
    if request.method == 'DELETE':
        book = get_book(isbn=isbn)

        book.delete()

        return Response(
            {
                'success':True,
                'message':'Book has been successfully deleted!'
            }, status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def filter_books_view(request):
    if request.method == 'GET':
        books = Book.objects.all()
        genre = request.query_params.get('genre')
        publisher = request.query_params.get('publisher')

        if not genre and not publisher:
            return Response(
                {
                    'success':False,
                    'message':'Please provide a filter query!'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if genre:
            books = books.filter(genre__iexact=genre)
        if publisher:
            books = books.filter(publisher__iexact=publisher)

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'message':'Filter results!',
                'book(s)':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def search_books_view(request):
    if request.method == 'GET':
        query = request.query_params.get('query')

        if not query:
            return Response(
                {
                    'success':False,
                    'message':'Provide a search query!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(genre__icontains=query)
        )

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'message':'Here are you search results',
                'book(s)':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsVerified])
def checkout_books_view(request, isbn:str): # borrow a book
    if request.method == 'POST':
        book = get_book(isbn=isbn)
        user = request.user

        checkout = CheckoutBook.objects.create(
            book=book,
            user=user
        )

        return Response(
            {
                'success':True,
                'message':f"The book '{book.title}' has been successfully checked out. Pick it up at the reception on your way out."
            }, status=status.HTTP_201_CREATED
        )
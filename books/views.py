from .models import Book, CheckoutBook, ReserveBook
from .serializers import BookSerializer, ReservesSerializer, CheckoutSerializer
from .utils import send_checkout_book_email
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


def get_reservation(id:str):
    try:
        reservation = ReserveBook.objects.get(reservation_id=id)
    except ReserveBook.DoesNotExist:
        return Response(
            {
                'success':False,
                'message':'Reservation does not exist!'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return reservation


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

        if CheckoutBook.objects.filter(user=user, book=book).exists():
            return Response(
                {
                    'success':False,
                    'message':'You have already borrowed this book!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        checkout = CheckoutBook.objects.create(
            book=book,
            user=user
        )
        send_checkout_book_email(email=user.email, username=user.username, book=book.title, borrow_date=str(checkout.borrow_date.date()), due_date=str(checkout.due_date.date()))

        return Response(
            {
                'success':True,
                'message':f"The book '{book.title}' has been successfully checked out. Pick it up at the reception on your way out."
            }, status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_books_borrowed_by_user_view(request):
    if request.method == 'GET':
        user = request.user

        if CheckoutBook.objects.filter(user=user).count() == 0:
            return Response(
                {
                    'success':True,
                    'message':'You have borrowed no books!'
                }, status=status.HTTP_200_OK
            )

        books = CheckoutBook.objects.filter(user=user)
        serializer = CheckoutSerializer(books, many=True)

        return Response(
            {
                'success':True,
                'books':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsVerified])
def reserve_book_view(request, isbn:str):
    if request.method == 'POST':
        user = request.user
        book = get_book(isbn=isbn)

        if book.available != 'Unavailable':
            return Response(
                {
                    'success':False,
                    'message':'This book is available'
                }, status=status.HTTP_403_FORBIDDEN
            )

        if ReserveBook.objects.filter(user=user, book=book).exists():
            return Response(
                {
                    'success':True,
                    'message':'This book is already in your reservations!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        reservation = ReserveBook.objects.create(book=book, user=user)

        return Response(
            {
                'success':True,
                'message':'This book has been added to your reservations. Check later to see if it is available'
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_all_reserved_books_view(request):
    if request.method == 'GET':
        user = request.user

        if ReserveBook.objects.filter(user=user).count() == 0:
            return Response(
                {
                    'success':True,
                    'message':'You have no books in your reservations!'
                }, status=status.HTTP_200_OK
            )
        
        reverses = ReserveBook.objects.filter(user=user)
        serializer = ReservesSerializer(reverses, many=True)

        return Response(
            {
                'success':True,
                'reserves':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def remove_book_from_reservations_view(request, id:str):
    if request.method == 'DELETE':
        user = request.user
        reservation = get_reservation(id=id)

        if user != reservation.user and user.is_staff != True:
            return Response(
                {
                    'success':False,
                    'message':'You do not have the permission to perform this action!'
                }, status=status.HTTP_403_FORBIDDEN
            )
        
        reservation.delete()

        return Response(
            {
                'success':True,
                'message':'The reservation has been successfully deleted!'
            },status=status.HTTP_204_NO_CONTENT
        )



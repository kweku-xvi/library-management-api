from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_books_view, name='get_all_books'),
    path('add', views.add_books_view, name='add_books'),
    path('filter', views.filter_books_view, name='filter_books'),
    path('search', views.search_books_view, name='search_books'),
    path('reserves', views.get_all_reserved_books_view, name='get_reserved_books'),
    path('borrowed-books', views.get_books_borrowed_by_user_view, name='get_borrowed_books'),
    path('<str:isbn>', views.get_book_details_view, name='get_particular_book'),
    path('<str:isbn>/update', views.update_book_details_view, name='update_book_details'),
    path('<str:isbn>/delete', views.delete_book_view, name='delete_book'),
    path('<str:isbn>/checkout', views.checkout_books_view, name='checkout_book'),
    path('<str:isbn>/reserve', views.reserve_book_view, name='reserve_book'),
    path('reserves/<uuid:id>/delete', views.remove_book_from_reservations_view, name='remove_reservation'),
]
from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_books_view, name='get_all_books'),
    path('add', views.add_books_view, name='add_books'),
    path('filter', views.filter_books_view, name='filter_books'),
    path('search', views.search_books_view, name='search_books'),
    path('<str:isbn>', views.get_book_details_view, name='get_particular_book'),
    path('<str:isbn>/update', views.update_book_details_view, name='update_book_details'),
    path('<str:isbn>/delete', views.delete_book_view, name='delete_book'),
    path('<str:isbn>/checkout', views.checkout_books_view, name='checkout_book'),
]
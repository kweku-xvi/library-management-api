from .models import Book, CheckoutBook, ReserveBook
from django.contrib import admin


admin.site.register(Book)
admin.site.register(CheckoutBook)
admin.site.register(ReserveBook)


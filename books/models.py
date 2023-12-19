import uuid
from accounts.models import User
from datetime import timedelta
from django.db import models
from django.utils import timezone


class Book(models.Model):
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable')
    ]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    authors = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    date_published =  models.DateField(default=timezone.now)
    publisher = models.CharField(max_length=255)
    number_of_pages = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=255)
    available = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES, default='Available')
    shelf_location = models.CharField(max_length=255, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)


class CheckoutBook(models.Model):
    checkout_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=(timezone.now() + timedelta(days=21)))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        ordering = ('-created_at',)


class ReserveBook(models.Model):
    reservation_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reserves')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} reserved "{self.book.title}"'

    class Meta:
        ordering = ('-created_at',)
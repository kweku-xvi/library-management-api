from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.user_signup_view, name='user_signup'),
    path('verify-user', views.verify_user_view, name='verify_user'),
    path('login', views.user_login_view, name='user_login'),
    path('password-reset', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm', views.password_reset_confirm_view, name='password_reset_confirm'),
    # path('<str:user_id>', views.get_user_details_view, name='get_user_details'),
    path('<str:user_id>/update-info', views.update_user_info_view, name='update_user_info'),
    path('users', views.get_all_users_view, name='get_all_users'),
    path('search', views.search_user_view, name='search_user'),
    path('filter', views.filter_users_view, name='filter_user')
]
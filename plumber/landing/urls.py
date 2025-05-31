from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_view, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('book-service', views.book_service, name='book_service'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),



    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),
    path('book_service/', views.book_service, name='book_service'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/', views.payment, name='payment'),
    path('login/', views.login, name='login'),


]

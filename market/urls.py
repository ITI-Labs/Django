from django.contrib import admin
from django.urls import path

from market import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('about/', views.about, name='about_page'),
    path('contact/', views.contact, name='contact_page'),
]
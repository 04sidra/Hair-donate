from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Donor related
    path('donor/register/', views.donor_registration, name='donor_registration'),
    path('donors/', views.donor_list, name='donor_list'),
    path('my-donations/', views.my_donations, name='my_donations'),
    
    # Request related
    path('request-hair/', views.request_hair, name='request_hair'),
    path('requests/', views.request_list, name='request_list'),
    path('request/<int:pk>/', views.request_detail, name='request_detail'),
    path('my-requests/', views.my_requests, name='my_requests'),
    
    # Other pages
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
]
from django.urls import path
from . import views
from .views import create_borrower, list_borrowers

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('search/', views.search_books, name='search_books'), # Search books page
    path('check/', views.check_in_out, name='check_in_out'), # Check in/out books page
    path('borrowers/new/', create_borrower, name='create_borrower'), # Create new borrower page
    path('borrowers/', list_borrowers, name='borrower_list'), # Borrower list page
    path("fines/", views.view_fines, name="view_fines"), # View fines page
    path("update_fines/", views.update_fines_view, name="update_fines"), # Update fines
    path("pay_fine/<str:card_id>/", views.pay_fine_view, name="pay_fine"), # Pay fine
]
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
	path('<str:username>/', views.account_view, name="view"),
    path('<str:username>/edit/', views.edit_account_view, name="edit"),
]
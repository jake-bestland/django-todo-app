from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
	path('<str:username>/', views.account_view, name="view"),	
]
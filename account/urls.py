from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
	path('<str:username>/', views.account_view, name="view"),
	# path('<user_id>/edit/', views.edit_account_view, name="edit"),
	# path('<user_id>/edit/cropImage/', views.crop_image, name="crop_image"),

	
]
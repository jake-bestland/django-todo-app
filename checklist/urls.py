from django.urls import path
from . import views


app_name = 'checklist'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]
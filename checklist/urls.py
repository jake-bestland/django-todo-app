from django.urls import path
from . import views


app_name = 'checklist'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
]
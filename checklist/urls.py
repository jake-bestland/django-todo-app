from django.urls import path
from . import views


app_name = 'checklist'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<str:username>/', views.UserChecklistListView.as_view(), name='my-lists'),
    path('<str:username>/<slug:slug>/', views.ChecklistDetailView.as_view(), name="checklist-detail"),
    path('<str:username>/add/', views.ChecklistCreate.as_view(), name="checklist-add"),
    path('<str:username>/<slug:slug>/entry/add', views.EntryCreate.as_view(), name="entry-add"),
    path('<str:username>/<slug:slug>/entry/<int:pk>/', views.EntryUpdate.as_view(), name="entry-update"),
]
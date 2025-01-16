from django.urls import path
from . import views


app_name = 'checklist'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<str:username>/mylists/', views.UserChecklistListView.as_view(), name='my-lists'),
    path('<str:username>/mylists/<int:checklist_id>/', views.ChecklistDetailView.as_view(), name="checklist-detail"),
    path('<str:username>/mylists/add/', views.ChecklistCreate.as_view(), name="checklist-add"),
    path('<str:username>/mylists/<int:checklist_id>/entry/add', views.EntryCreate.as_view(), name="entry-add"),
    path('<str:username>/mylists/<int:checklist_id>/entry/<int:pk>/', views.EntryUpdate.as_view(), name="entry-update"),
]
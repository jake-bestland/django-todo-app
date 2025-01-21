from django.urls import path
from . import views


app_name = 'checklist'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<str:username>/', views.UserChecklistListView.as_view(), name='index'),
    path('<str:username>/list/<int:list_id>/', views.EntryListView.as_view(), name="list"),

    path('<str:username>/list/add/', views.ChecklistCreate.as_view(), name="list-add"),
    path('<str:username>/list/<int:pk>/delete//', views.ChecklistDelete.as_view(), name="list-delete"),

    path('<str:username>/<int:list_id>/entry/add', views.EntryCreate.as_view(), name="entry-add"),
    path('<str:username>/<int:list_id>/entry/<int:pk>/', views.EntryUpdate.as_view(), name="entry-update"),
    path('<str:username>/list/<int:list_id>/entry/<int:pk>/delete/', views.EntryDelete.as_view(), name="entry-delete"),
]
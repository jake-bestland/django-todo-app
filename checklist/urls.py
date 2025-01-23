from django.urls import path
from . import views


# app_name = 'checklist'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<str:username>/', views.UserChecklistListView.as_view(), name='index'),
    path('<str:username>/<slug:slug>/', views.EntryListView.as_view(), name="list"),

    path('<str:username>/add-list/', views.create_checklist, name="list-add"),
    path('<str:username>/<slug:slug>/delete/', views.ChecklistDelete.as_view(), name="list-delete"),

    path('<str:username>/<slug:slug>/add-entry/', views.create_entry, name="entry-add"),
    path('<str:username>/<slug:slug>/<int:pk>/', views.update_entry, name="entry-update"),
    path('<str:username>/<slug:slug>/<int:pk>/delete/', views.EntryDelete.as_view(), name="entry-delete"),
    path('signout/', views.signout, name='signout'),
]
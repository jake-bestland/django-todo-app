from django.urls import path
from . import views


# app_name = 'checklist'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('<str:username>/', views.UserChecklistListView.as_view(), name='index'),
    path('<str:username>/view/<slug:slug>/', views.EntryListView.as_view(), name="list"),
    path('<str:username>/mark_complete/<int:pk>/', views.mark_complete, name="mark_complete"),
    path('<str:username>/mark_incomplete/<int:pk>/', views.mark_incomplete, name="mark_incomplete"),

    path('<str:username>/add-list/', views.ChecklistCreate.as_view(), name="add-list"),
    path('<str:username>/<slug:slug>/delete/', views.ChecklistDelete.as_view(), name="list-delete"),

    path('<str:username>/<slug:slug>/add-entry/', views.EntryCreate.as_view(), name="entry-add"),
    path('<str:username>/<slug:slug>/<int:pk>/', views.EntryUpdate.as_view(), name="entry-update"),
    path('<str:username>/<slug:slug>/<int:pk>/delete/', views.EntryDelete.as_view(), name="entry-delete"),
    path('signout/', views.signout, name='signout'),
]
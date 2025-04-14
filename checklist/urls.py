from django.urls import path
from . import views
# from friend.views import FriendsListView, send_friend_request, accept_friend_request, reject_friend_request

app_name = 'checklist'

urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('', views.UserChecklistListView.as_view(), name='index'),
    path('view/<slug:slug>/', views.EntryListView.as_view(), name="list"),

    path('add-list/', views.ChecklistCreate.as_view(), name="add-list"),
    path('<slug:slug>/delete/', views.ChecklistDelete.as_view(), name="list-delete"),

    path('<slug:slug>/add-entry/', views.EntryCreate.as_view(), name="entry-add"),
    path('<slug:slug>/<int:pk>/', views.EntryUpdate.as_view(), name="entry-update"),
    path('<slug:slug>/<int:pk>/delete/', views.EntryDelete.as_view(), name="entry-delete"),
]
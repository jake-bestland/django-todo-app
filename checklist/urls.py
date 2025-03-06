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
#     path('<str:username>/friends/', FriendsListView.as_view(), name='friends-list'),
#     path('<str:username>/send_friend_request/<int:receiver_id>/', send_friend_request, name='send_friend_request'),
#     path('<str:username>/accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
#     path('<str:username>/reject_friend_request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
]
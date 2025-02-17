from django.urls import path
from . import views


app_name = 'friend'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='all-users'),
    path('<str:username>/friends/', views.FriendsListView.as_view(), name='friends-list'),
    
    path('<str:username>/send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('<str:username>/accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('<str:username>/reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
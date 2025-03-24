from django.urls import path
from . import views


app_name = 'friend'

urlpatterns = [
    path('<str:username>', views.friends_list_view, name='friend-list'),
    path('friend_remove/', views.remove_friend, name='remove-friend'),
    path('send_friend_request/<str:receiver_username>', views.send_friend_request, name='send-friend-request'),
    path('friend_requests/<str:username>', views.friend_requests_list, name='friend-requests'),
    path('friend_request_accept/<friend_request_id>/', views.accept_friend_request, name='friend-request-accept'),
    path('friend_request_decline/<friend_request_id>/', views.decline_friend_request, name='friend-request-decline'),
    
    # path('<str:username>/send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    # path('<str:username>/accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    # path('<str:username>/reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
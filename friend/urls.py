from django.urls import path
from . import views


app_name = 'friend'

urlpatterns = [
    path('<str:username>', views.friends_list_view, name='friend-list'),
    path('friend_remove/<str:removee_username>', views.remove_friend, name='remove-friend'),
    path('send_friend_request/<str:receiver_username>', views.send_friend_request, name='send-friend-request'),
    path('friend_requests/<str:username>', views.friend_requests_list, name='friend-requests'),
    path('friend_request_accept/<int:friend_request_id>/', views.accept_friend_request, name='friend-request-accept'),
    path('friend_request_decline/<int:friend_request_id>/', views.decline_friend_request, name='friend-request-decline'),
    path('cancel_friend_request/<int:friend_request_id>/', views.cancel_friend_request, name='cancel-friend-request'),
]
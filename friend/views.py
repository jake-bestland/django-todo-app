from django.shortcuts import render, redirect, get_object_or_404
from checklist.models import Profile
from .models import FriendRequest
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
class FriendsListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'friend.friends_list.html'

@login_required
@api_view(['POST'])
def send_friend_request(request, receiver_id):
    sender = request.user
    receiver = get_object_or_404(Profile, id=receiver_id)
    if sender != receiver:
      friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
      if created:
        return Response({"message": "Friend request sent"})
      else:
        return Response({"message": "Friend request already sent"})
    else:
        return Response({"message": "Cannot send request to self"})

@login_required
@api_view(['GET'])
def list_pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    # Serialize and return the pending requests
    return Response(pending_requests)

@login_required
@api_view(['POST'])
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
    friend_request.status = 'accepted'
    friend_request.save()
    friend_request.receiver.friends.add(friend_request.sender)
    friend_request.sender.friends.add(friend_request.receiver)

    return Response({"message": "Friend request accepted"})

@login_required
@api_view(['POST'])
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
    friend_request.status = 'rejected'
    friend_request.save()
    return Response({"message": "Friend request rejected"})

@login_required
@api_view(['POST'])
def remove_friend(request, removee):
    """Initiate the action of unfriending someone."""
    remover = Profile.objects.get(user=request.user) # Person terminating the friendship
    # Remove friend from remover friend list
    remover.friends.remove(removee)
    # Remove friend from removee friend list
    removee_profile = Profile.objects.get(user=removee)
    removee_profile.friends.remove(remover)



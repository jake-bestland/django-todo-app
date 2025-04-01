from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from account.models import Account
from .models import FriendRequest, FriendList
from django.contrib.auth.decorators import login_required

# Create your views here.

def friends_list_view(request, username):
	"""View the friends of a user."""
	context = {}
	user = request.user
	this_user = get_object_or_404(Account, username=username)
	context['this_user'] = this_user
	if user.is_authenticated:
		if this_user:
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Could not find a friends list for {this_user.username}")
			
			if user != this_user:
				if not user in friend_list.friends.all():
					return HttpResponse("You must be friends to view their friends list.")
			friends = [] # [(friend1, True), (friend2, False), ...]
			# get the authenticated users friends list
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
	else:
		return HttpResponse("You must be friends to view their friends list.")
	return render(request, "friend/friends_list.html", context)

@login_required
def friend_requests_list(request, username):
	"""View a list of your friend requests."""
	user = request.user
	username = user.username
	friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
	friend_request_id = [request.id for request in friend_requests]
	context = {
		"friend_requests": friend_requests,
		"username": username,
		"friend_request_id": friend_request_id
		}

	return render(request, "friend/friend_requests.html", context)

@login_required
def send_friend_request(request, receiver_username):
	"""Create a FriendRequest."""
	context = {"receiver_username": receiver_username}
	if request.method == "POST":
		receiver = Account.objects.get(username=receiver_username)
		sender = request.user
		try:
			friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)
			try:
				for request in friend_requests:
					if request.is_active:
						raise Exception("You already sent them a request.")
				friend_request = FriendRequest(sender=sender, receiver=receiver)
				friend_request.save()
				return redirect("/")
			except Exception as e:
				return HttpResponse(f"Something went wrong: {str(e)}")
		except FriendRequest.DoesNotExist:
			friend_request = FriendRequest(sender=sender, receiver=receiver)
			friend_request.save()
			return redirect("/")
	return render(request, "friend/send_request.html", context)

@login_required
def accept_friend_request(request, friend_request_id):
	"""Accept a friend request that was sent to you."""
	if request.method == "POST":
		friend_request = get_object_or_404(FriendRequest, id=friend_request_id, receiver=request.user, is_active=True)
		friend_request.accept()
		return redirect('account:view', username=request.user.username)
	
	return redirect('account:view', username=request.user.username)

@login_required
def decline_friend_request(request, friend_request_id):
	"""Decline a friend request."""
	if request.method == "POST":
		friend_request = get_object_or_404(FriendRequest, id=friend_request_id, receiver=request.user, is_active=True)
		friend_request.decline()
		return redirect('account:view', username=request.user.username)
	
	return redirect('account:view', username=request.user.username)

@login_required
def cancel_friend_request(request, friend_request_id):
	"""Cancel a previously created friend request that you have sent."""
	if request.method == "POST":
		friend_request = FriendRequest.objects.get(id=friend_request_id)
		friend_request.cancel()
		return redirect('account:view', username=request.user.username)
	
	return redirect('account:view', username=request.user.username)

@login_required
def remove_friend(request, removee_username):
	"""Remove a user from your friends list."""
	if request.method == "POST":
		removee = get_object_or_404(Account, username=removee_username)
		friend_list = FriendList.objects.get(user=request.user)
		friend_list.unfriend(removee)
		return redirect('account:view', username=request.user.username)
	
	return redirect('account:view', username=request.user.username)

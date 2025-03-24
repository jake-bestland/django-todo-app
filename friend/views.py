from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import json
from account.models import Account
from .models import FriendRequest, FriendList
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# class FriendsListView(LoginRequiredMixin, generic.ListView):
#     model = FriendList
#     template_name = 'friend/friends_list.html'

def friends_list_view(request, username):
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

# def friend_requests(request, *args, **kwargs):
# 	""" View friend requests."""
# 	context = {}
# 	user = request.user
# 	if user.is_authenticated:
# 		username = kwargs.get("username")
# 		account = Account.objects.get(username=username)
# 		if account == user:
# 			friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
# 			context['friend_requests'] = friend_requests
# 		else:
# 			return HttpResponse("You can't view another users friend requests.")
# 	else:
# 		redirect("welcome")
# 	return render(request, "friend/friend_requests.html", context)

@login_required
def friend_requests_list(request, username):
	"""View friend requests."""
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

# @login_required
# def friend_request_detail(request, friend_request_id):
# 	"""View a particular friend request."""
# 	friend_request = get_object_or_404(FriendRequest, id=friend_request_id)

# 	return render(request, "friend/request_detail", {"friend_request": friend_request})


# def send_friend_request(request, *args, **kwargs):
#     user = request.user
#     if request.method == "POST" and user.is_authenticated:
#         username = request.POST.get("receiver_username")
#         if username:
#             receiver = Account.objects.get(username=username)
#             try:
#                 # Get any friend requests (active and not-active)
#                 friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
#                 # find if any of them are active (pending)
#                 try:
#                     for request in friend_requests:
#                         if request.is_active:
#                             raise Exception("You already sent them a friend request.")
#                     # If none are active create a new friend request
#                     friend_request = FriendRequest(sender=user, receiver=receiver)
#                     friend_request.save()
#                     return HttpResponse("Friend request sent.")
#                 except Exception as e:
#                     return HttpResponse(f"Something went wrong: {str(e)}")
#             except FriendRequest.DoesNotExist:
#                 # There are no friend requests so create one.
#                 friend_request = FriendRequest(sender=user, receiver=receiver)
#                 friend_request.save()
#                 return HttpResponse("Friend request sent.")
#         else:
#             return HttpResponse("Unable to sent a friend request.")
#     else:
#         return HttpResponse("You must be authenticated to send a friend request.")
#     # return HttpResponse(json.dumps(payload), content_type="application/json")


# def accept_friend_request(request, *args, **kwargs):
# 	user = request.user
# 	payload = {}
# 	if request.method == "GET" and user.is_authenticated:
# 		friend_request_id = kwargs.get("friend_request_id")
# 		if friend_request_id:
# 			friend_request = FriendRequest.objects.get(pk=friend_request_id)
# 			# confirm that is the correct request
# 			if friend_request.receiver == user:
# 				if friend_request: 
# 					# found the request. Now accept it
# 					updated_notification = friend_request.accept()
# 					payload['response'] = "Friend request accepted."

# 				else:
# 					payload['response'] = "Something went wrong."
# 			else:
# 				payload['response'] = "That is not your request to accept."
# 		else:
# 			payload['response'] = "Unable to accept that friend request."
# 	else:
# 		# should never happen
# 		payload['response'] = "You must be authenticated to accept a friend request."
# 	return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_friend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that friend."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to remove a friend."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def decline_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now decline it
					updated_notification = friend_request.decline()
					payload['response'] = "Friend request declined."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your friend request to decline."
		else:
			payload['response'] = "Unable to decline that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to decline a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")






@login_required
def send_friend_request(request, receiver_username):
	context = {"receiver_username": receiver_username}
	if request.method =="POST":
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
		


# @login_required
# def list_pending_friend_requests(request):
#     pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
#     # Serialize and return the pending requests
#     return Response(pending_requests)

@login_required
def accept_friend_request(request, friend_request_id):
	if request.method == "POST":
		friend_request = get_object_or_404(FriendRequest, id=friend_request_id, receiver=request.user, is_active=True)
		friend_request.accept()
		return redirect('account:view', username=request.user.username)
	
	return redirect('account:view', username=request.user.username)
    

# @login_required
# def reject_friend_request(request, request_id):
#     friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
#     friend_request.status = 'rejected'
#     friend_request.save()
#     return Response({"message": "Friend request rejected"})

# @login_required
# def remove_friend(request, removee):
#     """Initiate the action of unfriending someone."""
#     remover = Account.objects.get(user=request.user) # Person terminating the friendship
#     # Remove friend from remover friend list
#     remover.friends.remove(removee)
#     # Remove friend from removee friend list
#     removee_profile = Account.objects.get(user=removee)
#     removee_profile.friends.remove(remover)



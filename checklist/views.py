from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from checklist.forms import SignupForm, SigninForm #, NewChecklistForm, EntryForm
from .models import Checklist, Entry#, #Profile#, FriendRequest
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from account.models import Account
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# Create your views here.
# def homepage(request):
#     if request.user.is_authenticated:
#         return redirect('/' + request.user.username + '/')
#     else:
#         if request.method =='POST':
#             if 'signupform' in request.POST:
#                 signupform = SignupForm(data=request.POST)
#                 signinform = SigninForm()

#                 if signupform.is_valid():
#                     username = signupform.cleaned_data['username']
#                     password = signupform.cleaned_data['password1']
#                     signupform.save()
#                     user = authenticate(username=username, password=password)
#                     login(request, user)
#                     return redirect('/')
                
#             else:
#                 signinform = SigninForm(data=request.POST)
#                 signupform = SignupForm()

#                 if signinform.is_valid():
#                     login(request, signinform.get_user())
#                     return redirect('/')
                
#         else:
#             signupform = SignupForm()
#             signinform = SigninForm()

#     return render(request, 'checklist/homepage.html', {"signupform": signupform,
#                                                        "signinform": signinform})



# @login_required
# def create_checklist(request, username):
#     if request.user.is_authenticated:
#         user = User.objects.get(username=username)

#         if request.method == 'POST':
#             form = NewChecklistForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect("index", args=[user]) #Use success URL
#         else:
#             form = NewChecklistForm()

#         return render(request, 'checklist/checklist_form.html', {'form': form, 'user':user})
#     else:
#         return redirect('/')


class UserChecklistListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing checklists created by current user."""
    model = Checklist
    template_name = 'checklist/user_checklist_index.html'

    def get_queryset(self):
        """Return lists created by user."""
        return Checklist.objects.filter(author__username=self.request.user)

# class FriendsListView(LoginRequiredMixin, generic.ListView):
#     model = Profile
#     template_name = 'checklist.friends_list.html'

class EntryListView(LoginRequiredMixin, generic.ListView):
    model = Entry
    template_name = 'checklist/checklist.html'

    def get_queryset(self):
        return Entry.objects.filter(checklist__slug=self.kwargs["slug"])
    
    def get_context_data(self):
        context = super().get_context_data()
        context["checklist"] = Checklist.objects.get(slug=self.kwargs["slug"])
        return context



class ChecklistCreate(LoginRequiredMixin, generic.CreateView):
    model = Checklist
    fields = ["title", "author"]

    def get_initial(self):
        initial_data = super().get_initial()
        author = Account.objects.get(username=self.request.user)
        initial_data["author"] = author
        return initial_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new list."
        return context
    
    def get_success_url(self):
        return reverse("checklist:index")

class EntryCreate(LoginRequiredMixin, generic.CreateView):
    model = Entry
    fields = [
        "checklist",
        "name",
    ]

    def get_initial(self):
        initial_data = super().get_initial()
        checklist = Checklist.objects.get(slug=self.kwargs["slug"])
        initial_data["checklist"] = checklist
        return initial_data
    
    def get_context_data(self):
        context = super().get_context_data()
        checklist = Checklist.objects.get(slug=self.kwargs["slug"])
        context["checklist"] = checklist
        context["name"] = "Create a new entry"
        return context
    
    def get_success_url(self):
        return reverse("checklist:list", args=[self.object.checklist.slug])

class EntryUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Entry
    fields = [
        "checklist",
        "name",
    ]

    def get_context_data(self):
        context = super().get_context_data()
        context["checklist"] = self.object.checklist
        context["name"] = "Edit entry"
        return context
    
    def get_success_url(self):
        return reverse("checklist:list", args=[self.object.checklist.slug])


class ChecklistDelete(LoginRequiredMixin, generic.DeleteView):
    model = Checklist

    def get_success_url(self):
        return reverse_lazy("checklist:index")


class EntryDelete(LoginRequiredMixin, generic.DeleteView):
    model = Entry

    def get_success_url(self):
        return reverse_lazy("checklist:list", args=[self.object.checklist.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist"] = self.object.checklist
        return context

# @login_required
# @api_view(['POST'])
# def send_friend_request(request, receiver_id):
#     sender = request.user
#     receiver = get_object_or_404(Profile, id=receiver_id)
#     if sender != receiver:
#       friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
#       if created:
#         return Response({"message": "Friend request sent"})
#       else:
#         return Response({"message": "Friend request already sent"})
#     else:
#         return Response({"message": "Cannot send request to self"})

# @login_required
# @api_view(['GET'])
# def list_pending_friend_requests(request):
#     pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
#     # Serialize and return the pending requests
#     return Response(pending_requests)

# @login_required
# @api_view(['POST'])
# def accept_friend_request(request, request_id):
#     friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
#     friend_request.status = 'accepted'
#     friend_request.save()
#     friend_request.receiver.friends.add(friend_request.sender)
#     friend_request.sender.friends.add(friend_request.receiver)

#     return Response({"message": "Friend request accepted"})

# @login_required
# @api_view(['POST'])
# def reject_friend_request(request, request_id):
#     friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user, status='pending')
#     friend_request.status = 'rejected'
#     friend_request.save()
#     return Response({"message": "Friend request rejected"})

# @login_required
# @api_view(['POST'])
# def remove_friend(request, removee):
#     """Initiate the action of unfriending someone."""
#     remover = Profile.objects.get(user=request.user) # Person terminating the friendship
#     # Remove friend from remover friend list
#     remover.friends.remove(removee)
#     # Remove friend from removee friend list
#     removee_profile = Profile.objects.get(user=removee)
#     removee_profile.friends.remove(remover)



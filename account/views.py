from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.conf import settings
from .forms import SignupForm, SigninForm, AccountUpdateForm
from .models import Account
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def welcome(request):
    if request.user.is_authenticated:
        return redirect(reverse("account:view", args=[request.user.username]))
    else:
        if request.method =='POST':
            if 'signupform' in request.POST:
                signupform = SignupForm(data=request.POST)
                signinform = SigninForm()

                if signupform.is_valid():
                    username = signupform.cleaned_data['username']
                    password = signupform.cleaned_data['password1']
                    signupform.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('/')
                
            else:
                signinform = SigninForm(data=request.POST)
                signupform = SignupForm()

                if signinform.is_valid():
                    login(request, signinform.get_user())
                    return redirect('/')
                
        else:
            signupform = SignupForm()
            signinform = SigninForm()

    return render(request, 'account/welcome.html', {"signupform": signupform,
                                                       "signinform": signinform})


def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        if 'q' in request.GET:
            search_query = request.GET['q']
            if len(search_query) > 0:
                multiple_q = Q(Q(email__icontains=search_query) | Q(username__icontains=search_query))
                search_results = Account.objects.filter(multiple_q)
                # search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
                user = request.user
                accounts = [] # [(account1, True), (account2, False), ...]
                if user.is_authenticated:
                    # get the authenticated users friend list
                    auth_user_friend_list = FriendList.objects.get(user=user)
                    for account in search_results:
                        accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                    context['accounts'] = accounts
                else:
                    for account in search_results:
                        accounts.append((account, False))
                    context['accounts'] = accounts
        
        
    return render(request, "account/search_results.html", context)



def account_view(request, *args, **kwargs):
    """L"""
    context = {}
    username = kwargs.get("username")
    try:
        account = Account.objects.get(username=username)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['profile_image'] = account.profile_image
        context['hide_email'] = account.hide_email

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        # Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(username=user.username):
                is_friend = True
            else:
                is_friend = False
                # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                    context['friend_request_id'] = get_friend_request_or_false(sender=user, receiver=account).id
                # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "account/account.html", context)
    
@login_required
def edit_account_view(request, username):
    account = Account.objects.get(username=username)
    if account.pk != request.user.pk:
           messages.success(request, ("You cannot edit someone elses profile."))
           return redirect("account:view", username=request.user.username)
    context = {}
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
           form.save()

           messages.success(request, ("Your Profile Has Been Updated!"))
           return redirect("account:view", username=request.user.username)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                                     initial={
                                          "id": account.pk,
                                          "email": account.email,
                                          "username": account.username,
                                          "profile_image": account.profile_image,
                                          "hide_email": account.hide_email,
                                          }
                                          )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                "id": account.pk,
                "email": account.email,
                "username": account.username,
                "profile_image": account.profile_image,
                "hide_email": account.hide_email,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_account.html", context)
            

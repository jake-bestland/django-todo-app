from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from checklist.forms import SignupForm, SigninForm
from .models import Checklist
from django.views import generic

# Create your views here.
# class HomePageView(generic.ListView):
#     model = Checklist
#     template_name = 'checklist/homepage.html'

def homepage(request):
    if request.user.is_authenticated:
        return redirect('/' + request.user.username + '/')
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

    return render(request, 'checklist/homepage.html', {'signupform': signupform,
                                              'signinform': signinform})
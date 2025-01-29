from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from checklist.forms import SignupForm, SigninForm
from .models import Checklist, Entry, Profile
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
# from .forms import NewChecklistForm#, EntryForm

# Create your views here.
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

@login_required
def signout(request):
    logout(request)
    return redirect('/')

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

# @login_required
# def create_entry(request, username, slug):
#     if request.user.is_authenticated:
#         user = User.objects.get(username=username)
#         if request.method == 'POST':
#             form = EntryForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('/' + username + '/' + str(slug) + '/add-entry/') #Use success URL
#         else:
#             form = EntryForm()

#         return render(request, 'checklist/entry_form.html', {'form': form})
#     else:
#         return redirect('/')

# @login_required
# def update_entry(request, pk):
#     entry_instance = get_object_or_404(Entry, pk=pk)

#     if request.method == 'POST':
#         form = EntryForm(request.POST, instance=entry_instance)
#         if form.is_valid():
#             form.save()
#             return redirect('list') #Use success URL
#     else:
#         form = EntryForm(instance=entry_instance)

#     return render(request, 'checklist/entry_form.html', {'form': form})

class UserChecklistListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing checklists created by current user."""
    model = Checklist
    template_name = 'checklist/user_checklist_index.html'

    def get_queryset(self):
        """Return lists created by user."""
        return Checklist.objects.filter(author__user=self.request.user)

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
        author = Profile.objects.get(user=self.request.user)
        initial_data["author"] = author
        return initial_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new list."
        return context
    
    def get_success_url(self):
        return reverse("index", args=[self.request.user])

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
        return reverse("list", args=[self.request.user, self.object.checklist.slug])

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
        return reverse("list", args=[self.request.user, self.object.checklist.slug])


class ChecklistDelete(LoginRequiredMixin, generic.DeleteView):
    model = Checklist

    def get_success_url(self):
        return reverse_lazy("index", args=[self.request.user])


class EntryDelete(LoginRequiredMixin, generic.DeleteView):
    model = Entry

    def get_success_url(self):
        return reverse_lazy("list", args=[self.request.user, self.object.checklist.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist"] = self.object.checklist
        return context

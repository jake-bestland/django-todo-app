from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from checklist.forms import SignupForm, SigninForm
from .models import Checklist, Entry
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin #, PermissionRequiredMixin
from django.urls import reverse

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return redirect('/' + request.user.username + '/mylists')
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


class UserChecklistListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing checklists created by current user."""
    model = Checklist
    template_name = 'checklist/user_checklist_index.html'

    def get_queryset(self):
        """Return lists created by user."""
        return Checklist.objects.filter(author=self.request.user).order_by('-pub_date')

class ChecklistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Entry
    template_name = 'checklist/checklist_detail.html'

    def get_queryset(self):
        return Entry.objects.filter(checklist_id=self.kwargs["checklist_id"])
    
    def get_context_data(self):
        context = super().get_context_data()
        context["checklist"] = Checklist.objects.get(id=self.kwargs["checklist_id"])
        return context

class ChecklistCreate(LoginRequiredMixin, generic.CreateView):
    model = Checklist
    fields = ["title"]
    
    def get_context_data(self):
        context = super(ChecklistCreate, self).get_context_data()
        context["title"] = "Add a new list."
        return context
    
class EntryCreate(LoginRequiredMixin, generic.CreateView):
    model = Entry
    fields = [
        "checklist",
        "name",
        "notes",
    ]

    def get_initial(self):
        initial_data = super(EntryCreate, self).get_initial()
        checklist = Checklist.objects.get(id=self.kwargs["checklist_id"])
        initial_data["checklist"] = checklist
        return initial_data
    
    def get_context_data(self):
        context = super(EntryCreate, self).get_context_data()
        checklist = Checklist.objects.get(id=self.kwargs["checklist_id"])
        context["checklist"] = checklist
        context["name"] = "Create a new item"
        return context
    
    def get_success_url(self):
        return reverse("checklist-detail", args=[self.object.checklist_id])

class EntryUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Entry
    fields = [
        "checklist",
        "name",
        "notes",
    ]

    def get_context_data(self):
        context = super(EntryUpdate, self).get_context_data()
        context["checklist"] = self.object.checklist
        context["name"] = "Edit entry"
        return context
    
    def get_success_url(self):
        return reverse("checklist-detail", args=[self.object.checklist_id])


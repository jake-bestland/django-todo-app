from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from checklist.forms import SignupForm, SigninForm
from .models import Checklist, Entry
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import NewChecklistForm, EntryForm

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

@login_required
def create_checklist(request):
    if request.method == 'POST':
        form = NewChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') #Use success URL
    else:
        form = NewChecklistForm()

    return render(request, 'checklist_form.html', {'form': form})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list') #Use success URL
    else:
        form = EntryForm()

    return render(request, 'entry_form.html', {'form': form})

@login_required
def update_entry(request, pk):
    entry_instance = get_object_or_404(Entry, pk=pk)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry_instance)
        if form.is_valid():
            form.save()
            return redirect('list') #Use success URL
    else:
        form = EntryForm(instance=entry_instance)

    return render(request, 'entry_form.html', {'form': form})

class UserChecklistListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing checklists created by current user."""
    model = Checklist
    template_name = 'checklist/user_checklist_index.html'

    # def get_queryset(self):
    #     """Return lists created by user."""
    #     return Checklist.objects.filter(author=self.request.user).order_by('-pub_date')

class EntryListView(LoginRequiredMixin, generic.ListView):
    model = Entry
    template_name = 'checklist/checklist.html'

    def get_queryset(self):
        return Entry.objects.filter(checklist_id=self.kwargs["list_id"])
    
    def get_context_data(self):
        context = super().get_context_data()
        context["checklist"] = Checklist.objects.get(id=self.kwargs["list_id"])
        return context



# class ChecklistCreate(LoginRequiredMixin, generic.CreateView):
#     model = Checklist
#     fields = ["title"]
    
#     def get_context_data(self):
#         context = super().get_context_data()
#         context["title"] = "Add a new list."
#         return context
    
# class EntryCreate(LoginRequiredMixin, generic.CreateView):
#     model = Entry
#     fields = [
#         "checklist",
#         "name",
#         "notes",
#     ]

#     def get_initial(self):
#         initial_data = super().get_initial()
#         checklist = Checklist.objects.get(id=self.kwargs["checklist_id"])
#         initial_data["checklist"] = checklist
#         return initial_data
    
#     def get_context_data(self):
#         context = super().get_context_data()
#         checklist = Checklist.objects.get(id=self.kwargs["checklist_id"])
#         context["checklist"] = checklist
#         context["name"] = "Create a new item"
#         return context
    
#     def get_success_url(self, username):
#         user = User.objects.get(username=username)
#         return redirect('/' + user.username +)

# class EntryUpdate(LoginRequiredMixin, generic.UpdateView):
#     model = Entry
#     fields = [
#         "checklist",
#         "name",
#         "notes",
#     ]

#     def get_context_data(self):
#         context = super().get_context_data()
#         context["checklist"] = self.object.checklist
#         context["name"] = "Edit entry"
#         return context
    
#     def get_success_url(self):
#         return reverse("list", args=[self.object.checklist_id])


class ChecklistDelete(LoginRequiredMixin, generic.DeleteView):
    model = Checklist
    success_url = reverse_lazy("index")


class EntryDelete(LoginRequiredMixin, generic.DeleteView):
    model = Entry

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist"] = self.object.checklist
        return context

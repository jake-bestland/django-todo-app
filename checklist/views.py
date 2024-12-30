from django.shortcuts import render
from .models import Checklist
from django.views import generic

# Create your views here.
class HomePageView(generic.ListView):
    model = Checklist
    template_name = 'checklist/homepage.html'
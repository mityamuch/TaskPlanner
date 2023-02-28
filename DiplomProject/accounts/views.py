from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def start(request):
    return render(request, "signup")


def redirect_to_tasks(request):
    return redirect('todo:home', permanent=False)


def home(request):
    return render(request, "index.html")

# Create your views here.

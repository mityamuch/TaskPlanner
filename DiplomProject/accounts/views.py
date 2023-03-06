from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import UserUpdateForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def start(request):
    return render(request, "signup")


def redirect_to_login(request):
    return redirect('login', permanent=False)


def redirect_to_tasks(request):
    return redirect('todo:home', permanent=False)


def home(request):
    user = request.user
    context = {'user': user}
    return render(request, "index.html",context)


def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    context = {
        'user_form': user_form,
    }

    return render(request, 'profile_edit.html', context)

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html", context)

def about(request):
    context = {}
    return render(request, "about.html", context)

def signin(request):
    if request.user.is_authenticated:
        return redirect(reverse('home:index'))

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home:index'))
            else:
                messages.error(request, "Invalid username and password.")
        else:
            messages.error(request, form.errors)
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect(reverse('home:index'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home:index'))
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'signup.html', context)

def events(request):
    context = {}
    return render(request, "events.html", context)    

def dashboard(request):
    context = {}
    return render(request, "dashboard.html", context)

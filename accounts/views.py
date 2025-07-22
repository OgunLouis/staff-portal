from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import StaffSignupForm, StaffUpdateForm
from .models import Salary
from .utils import upload_to_imagekit
from django.conf import settings

def home(request):
    return render(request, 'accounts/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = StaffSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid login details'
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    salary = Salary.objects.filter(user=request.user).first()  # Safe fetch
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'salary': salary
    })

@login_required
def edit_profile_view(request):
    print("🔍 Current storage:", settings.DEFAULT_FILE_STORAGE)

    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Upload photo to ImageKit manually
            photo = request.FILES.get('image')
            if photo:
                uploaded_url = upload_to_imagekit(photo)
                if uploaded_url:
                    user.photo = uploaded_url

            user.save()
            return redirect('profile')
    else:
        form = StaffUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

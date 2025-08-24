# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages  # optional for flash messages

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UploadForm, RegisterForm
from .models import UploadedFile

# 🟢 SIGN IN (Login)
def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'signin.html')  # reload with error
    return render(request, 'signin.html')


# 🔴 LOGOUT
def signout_view(request):
    logout(request)
    messages.info(request, "🔒 You have been signed out.")
    return redirect('signin')  # go back to login after logout


# 🟡 Optional: SIGN UP
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request,"Account created successfully")
            return redirect('signin')
    return render(request, 'signup.html')


# 🏠 HOME (After login)
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'home.html', {'user': request.user})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def upload_file(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            return redirect('home')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def home_view(request):
    # files = UploadedFile.objects.all().order_by('-uploaded_at')
    # return render(request, 'home.html', {'files': files})

    department = request.GET.get('department')
    year = request.GET.get('year')

    notes = UploadedFile.objects.all().order_by("department","year","uploaded_at")

    if department:
        notes = notes.filter(department=department)
    if year:
        notes = notes.filter(year=year)

    context = {
        'files': notes,
        'department': department,
        'year': year
    }
    return render(request, 'home.html', context)




from django.shortcuts import get_object_or_404

@login_required
def delete_file(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)

    # Only allow the user who uploaded or admin to delete
    if request.user == file.uploaded_by or request.user.is_superuser:
        file.file.delete()  # Deletes the actual file from filesystem
        file.delete()       # Deletes the database entry

    return redirect('home')

    
from django.shortcuts import HttpResponse
from django.http import FileResponse, Http404
import mimetypes
import os


@login_required
def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    file_path = uploaded_file.file.path
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    response = FileResponse(open(file_path, 'rb'), content_type=mime_type or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def about(request):
    return render(request,"about.html") 

def error(request):
    return render(request,'404.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user.user_type)
            login(request, user)
            if user.user_type == "student":
                return redirect('students_workspaces')
            elif user.user_type == "teacher":
                return redirect('teachers_workspaces')
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password.'})

    return render(request=request, template_name="auth/login.html")


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password :
            user.set_password(password)
        user.save()
        return render(request, 'auth/profile.html')
    else:
        return render(request=request, template_name="auth/profile.html", context={"user": user})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user.user_type)
        if user is not None:
            login(request, user)
            if user.user_type == "student":
                return redirect('students_workspaces')
            elif user.user_type == "teacher":
                return redirect('teachers_workspaces')
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request=request, template_name="login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
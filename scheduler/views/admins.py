from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from django.core.paginator import Paginator
from django.urls import reverse


CustomUser = get_user_model()


@login_required
@admin_required
def admins_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_superuser=True, user_type='admin')
            print(user)
            return redirect('admins')
        except Exception as e:
            print(e)
            return redirect(reverse('admins') + '?error=An+error+occurred+while+creating+the+profile')

    else:
        error = request.GET.get('error')
        admins = CustomUser.objects.filter(is_superuser=True).order_by('username')
        paginator = Paginator(admins, 20)
        page_number = request.GET.get('page')
        admins = paginator.get_page(page_number)

        admins_context = {
            'admins': admins,
            "error": error
        }
        return render(request=request, template_name="admins/home.html", context=admins_context)


@login_required
@admin_required
def admin_details_view(request, admin_id):
    admin = get_object_or_404(CustomUser, id=admin_id)

    if admin.user_type != "admin" and not admin.is_superuser:
        return render(request, 'admins/home.html', {'error': 'The requested user is not an admin'})

    if request.method == 'POST' and request.POST["_method"] == "delete":
        admin.delete()
        return redirect('admins')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            admin.username = username
            admin.first_name = first_name
            admin.last_name = last_name
            admin.email = email
            admin.save()
            return redirect('admins')
        except Exception as e:
            print(e)
            return redirect(reverse('admins') + '?error=An+error+occurred+while+updating+the+profile')
    elif request.method == 'GET':
        error = request.GET.get('error')
        admin_context = {
            'admin': admin,
            'error': error,
        }
        return render(request=request, template_name="admins/details.html", context=admin_context)

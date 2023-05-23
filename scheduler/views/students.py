from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required
from ..models import Etudiant, Formation, Section, Groupe
from django.core.paginator import Paginator

CustomUser = get_user_model()


@login_required
@student_required
def students_home_view(request):
    print(request.user)
    home_context = {
        "user": request.user
    }
    return render(request=request, template_name="students/workspace.html", context=home_context)


@login_required
@admin_required
def students_view(request):
    if request.method == 'POST':
        # form = StudentForm(request.POST)
        # print(form)
        # if form.is_valid():
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type='student')
        print(user)

        selected_group_id = request.POST.get('group')
        selected_group = Groupe.objects.get(id=selected_group_id)
        print(selected_group)

        etudiant = Etudiant.objects.create(user=user, groupe=selected_group)
        print(etudiant)
        # form.instance.user = user
        # form.instance.groupe = selected_group
        # form.save()
        return redirect('students')

    else:
        groups = Groupe.objects.all()
        students = Etudiant.objects.all()

        paginator = Paginator(students, 20)
        page_number = request.GET.get('page')
        students = paginator.get_page(page_number)

        students_context = {
            'groups': groups,
            'students': students,
        }
        return render(request=request, template_name="students/home.html", context=students_context)


@login_required
@admin_required
def student_details_view(request, student_id):
    student = get_object_or_404(Etudiant, user_id=student_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        student.delete()
        return redirect('students')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        username = request.POST['username']
        group_id = request.POST['group']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        student.user.username = username
        student.user.first_name = first_name
        student.user.last_name = last_name
        student.user.email = email
        student.user.save()

        student.groupe_id = group_id
        student.save()
        return redirect('student_details', student_id=student_id)
    elif request.method == 'GET':
        groups = Groupe.objects.all()
        student_context = {
            'student': student,
            "groups": groups
        }
        return render(request=request, template_name="students/details.html", context=student_context)

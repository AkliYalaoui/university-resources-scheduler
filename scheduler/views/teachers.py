from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance, Grade
from django.core.paginator import Paginator

CustomUser = get_user_model()


@login_required
@teacher_required
def teachers_home_view(request):
    teacher = get_object_or_404(Enseignant, user_id=request.user.id)
    teacher_modules = teacher.modules.all
    days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']

    selected_semester_id = request.GET.get('semester')
    selected_semester = None
    if selected_semester_id:
        selected_semester = Semestre.objects.get(id=selected_semester_id)
    semesters = Semestre.objects.all()
    seances = Seance.objects.filter(
        enseignant=teacher, semester=selected_semester).order_by('start_time')

    dimanche = seances.filter(day="dimanche")
    lundi = seances.filter(day="lundi")
    mardi = seances.filter(day="mardi")
    mercredi = seances.filter(day="mercredi")
    jeudi = seances.filter(day="jeudi")

    teacher_context = {
        "teacher": teacher,
        "teacher_modules": teacher_modules,
        "days": days,
        "semesters": semesters,
        "selected_semester": selected_semester,
        'dimanche': dimanche,
        'lundi': lundi,
        'mardi': mardi,
        'mercredi': mercredi,
        'jeudi': jeudi,
    }
    return render(request=request, template_name="teachers/workspace.html", context=teacher_context)


@login_required
@admin_required
def teachers_view(request):
    if request.method == 'POST':
        # form = StudentForm(request.POST)
        # print(form)
        # if form.is_valid():
        username = request.POST['username']
        grade_id = request.POST['grade']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type='teacher')
        print(user)

        grade = Grade.objects.get(id=grade_id)
        teacher = Enseignant.objects.create(user=user, grade=grade)
        print(teacher)
        # form.instance.user = user
        # form.instance.groupe = selected_group
        # form.save()
        return redirect('teachers')

    else:
        teachers = Enseignant.objects.all()
        grades = Grade.objects.all()
        paginator = Paginator(teachers, 20)
        page_number = request.GET.get('page')
        teachers = paginator.get_page(page_number)
        teachers_context = {
            'teachers': teachers,
            'grades': grades,
        }
        return render(request=request, template_name="teachers/home.html", context=teachers_context)


@login_required
@admin_required
def teacher_details_view(request, teacher_id):
    teacher = get_object_or_404(Enseignant, user_id=teacher_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        teacher.delete()
        if request.POST["_redirect"]:
            return redirect(request.POST["_redirect"])
        return redirect('teachers')
    
    elif request.method == 'POST' and request.POST["_method"] == "put":
        username = request.POST['username']
        grade_id = request.POST['grade']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        teacher.user.username = username
        teacher.user.first_name = first_name
        teacher.user.last_name = last_name
        teacher.user.email = email
        teacher.user.save()

        grade = Grade.objects.get(id=grade_id)
        teacher.grade = grade
        teacher.save()
        return redirect('teacher_details', teacher_id=teacher_id)
    elif request.method == 'POST' and request.POST["_method"] == "post":
        selected_modules = request.POST.getlist("modules")
        teacher.modules.set(selected_modules)
        teacher.save()
        return redirect('teacher_details', teacher_id=teacher_id)
    elif request.method == 'GET':
        modules = Module.objects.all()
        grades = Grade.objects.all()
        teacher_modules = teacher.modules.all
        print(teacher_modules)
        teacher_context = {
            'teacher': teacher,
            "teacher_modules": teacher_modules,
            "modules": modules,
            "grades": grades,
        }
        return render(request=request, template_name="teachers/details.html", context=teacher_context)

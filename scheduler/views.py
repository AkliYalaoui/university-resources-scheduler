from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, student_required, teacher_required
from .models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from .forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm

CustomUser = get_user_model()


@login_required
@admin_required
def home_view(request):
    print(request.user)
    home_context = {
        "user": request.user
    }
    return render(request=request, template_name="home.html", context=home_context)

@login_required
@student_required
def students_home_view(request):
    print(request.user)
    home_context = {
        "user": request.user
    }
    return render(request=request, template_name="students/workspace.html", context=home_context)

@login_required
@teacher_required
def teachers_home_view(request):
    print(request.user)
    home_context = {
        "user": request.user
    }
    return render(request=request, template_name="teachers/workspace.html", context=home_context)


@login_required
@admin_required
def programs_view(request, group_id):
    group = Groupe.objects.get(id=group_id)
    times = ['08:00', '09:30', '11:00', '12:30',
             '14:00', '15:30', '17:00', '18:30']
    days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']

    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('programs', group_id=group.pk)
    else:
        selected_semester_id = request.GET.get('semester')
        selected_semester = None
        if selected_semester_id : 
            selected_semester = Semestre.objects.get(id=selected_semester_id)
        semesters = Semestre.objects.all()
        salles = Salle.objects.all()
        modules = Module.objects.filter(formation=group.section.formation, semester=selected_semester)
        teachers = Enseignant.objects.all()
        programs = Seance.objects.filter(groupe=group, semester=selected_semester)
        program_context = {'programs': programs,
                           "group": group, 
                           "times": times, 
                           "days": days, 
                           "salles": salles, 
                           "modules": modules, 
                           "teachers": teachers,
                           "semesters": semesters,
                           "selected_semester": selected_semester
                        }
        return render(request, 'programs.html', context=program_context)


@login_required
@admin_required
def formations_view(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formations')

    else:
        formations = Formation.objects.all()
        formations_context = {
            "formations": formations
        }
        return render(request=request, template_name="formations.html", context=formations_context)


@login_required
@admin_required
def semesters_view(request):
    if request.method == 'POST':
        form = SemestreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semesters')

    else:
        semesters = Semestre.objects.all()
        semesters_context = {
            "semesters": semesters
        }
        return render(request=request, template_name="semesters.html", context=semesters_context)


@login_required
@admin_required
def salles_view(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salles')

    else:
        salles = Salle.objects.all()
        salles_context = {
            "salles": salles
        }
        return render(request=request, template_name="salles.html", context=salles_context)


@login_required
@admin_required
def sections_view(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        print(form)
        if form.is_valid():
            selected_formation_id = request.POST.get('formation')
            selected_formation = Formation.objects.get(
                id=selected_formation_id)
            form.instance.formation = selected_formation
            form.save()
            return redirect('sections')

    else:
        selected_formation_id = request.GET.get('formation')
        selected_formation = None
        sections = None
        if selected_formation_id:
            selected_formation = Formation.objects.get(
                id=selected_formation_id)
            sections = Section.objects.filter(formation=selected_formation)

        formations = Formation.objects.all()
        formations_context = {
            'formations': formations,
            'selected_formation': selected_formation,
            'sections': sections,
        }
        return render(request=request, template_name="sections.html", context=formations_context)


@login_required
@admin_required
def groups_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        print(form)
        if form.is_valid():
            selected_section_id = request.POST.get('section')
            selected_section = Section.objects.get(id=selected_section_id)
            form.instance.section = selected_section
            form.save()
            return redirect('groups')

    else:
        selected_formation_id = request.GET.get('formation')
        selected_section_id = request.GET.get('section')
        selected_formation = None
        selected_section = None
        sections = None
        groups = None
        if selected_formation_id:
            selected_formation = Formation.objects.get(
                id=selected_formation_id)
            sections = Section.objects.filter(formation=selected_formation)
        if selected_section_id:
            selected_section = Section.objects.get(id=selected_section_id)
            groups = Groupe.objects.filter(section=selected_section)

        formations = Formation.objects.all()
        groups_context = {
            'formations': formations,
            'selected_formation': selected_formation,
            'selected_section': selected_section,
            'sections': sections,
            'groups': groups,
        }
        return render(request=request, template_name="groups.html", context=groups_context)


@login_required
@admin_required
def modules_view(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        print(form)
        if form.is_valid():
            selected_formation_id = request.POST.get('formation')
            selected_semester_id = request.POST.get('semester')
            selected_formation = Formation.objects.get(
                id=selected_formation_id)
            selected_semester = Semestre.objects.get(id=selected_semester_id)
            form.instance.formation = selected_formation
            form.instance.semester = selected_semester
            form.save()
            return redirect('modules')

    else:
        selected_formation_id = request.GET.get('formation')
        selected_semester_id = request.GET.get('semester')
        selected_formation = None
        selected_semester = None
        semesters = None
        modules = None
        if selected_formation_id:
            selected_formation = Formation.objects.get(
                id=selected_formation_id)
        if selected_semester_id:
            selected_semester = Semestre.objects.get(id=selected_semester_id)

        if selected_formation_id and selected_semester_id:
            try:
                modules = Module.objects.filter(
                    formation=selected_formation, semester=selected_semester)
            except:
                pass

        formations = Formation.objects.all()
        semesters = Semestre.objects.all()

        modules_context = {
            'formations': formations,
            'selected_formation': selected_formation,
            'selected_semester': selected_semester,
            'semesters': semesters,
            'modules': modules,
        }
        return render(request=request, template_name="modules.html", context=modules_context)


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
        selected_formation_id = request.GET.get('formation')
        selected_section_id = request.GET.get('section')
        selected_group_id = request.GET.get('group')
        selected_formation = None
        selected_section = None
        selected_group = None
        sections = None
        groups = None
        students = None

        if selected_formation_id:
            selected_formation = Formation.objects.get(
                id=selected_formation_id)
            sections = Section.objects.filter(formation=selected_formation)
        if selected_section_id:
            selected_section = Section.objects.get(id=selected_section_id)
            groups = Groupe.objects.filter(section=selected_section)
        if selected_group_id:
            selected_group = Groupe.objects.get(id=selected_group_id)
            students = Etudiant.objects.filter(groupe=selected_group)

        formations = Formation.objects.all()

        students_context = {
            'formations': formations,
            'selected_formation': selected_formation,
            'selected_section': selected_section,
            'selected_group': selected_group,
            'sections': sections,
            'groups': groups,
            'students': students,
        }
        return render(request=request, template_name="students/home.html", context=students_context)


@login_required
@admin_required
def teachers_view(request):
    if request.method == 'POST':
        # form = StudentForm(request.POST)
        # print(form)
        # if form.is_valid():
        username = request.POST['username']
        grade = request.POST['grade']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type='teacher')
        print(user)

        teacher = Enseignant.objects.create(user=user, grade=grade)
        print(teacher)
        # form.instance.user = user
        # form.instance.groupe = selected_group
        # form.save()
        return redirect('teachers')

    else:
        teachers = Enseignant.objects.all()
        teachers_context = {
            'teachers': teachers,
        }
        return render(request=request, template_name="teachers/home.html", context=teachers_context)
    
@login_required
@admin_required
def teacher_details_view(request, teacher_id):
    teacher = get_object_or_404(Enseignant, user_id=teacher_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        teacher.delete()
        return redirect('teachers')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        username = request.POST['username']
        grade = request.POST['grade']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        teacher.user.username = username
        teacher.user.first_name = first_name
        teacher.user.last_name = last_name
        teacher.user.email = email
        teacher.user.save()

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
        teacher_modules = teacher.modules.all
        print(teacher_modules)
        teacher_context = {
            'teacher': teacher,
            "teacher_modules": teacher_modules,
            "modules" : modules
        }
        return render(request=request, template_name="teachers/details.html", context=teacher_context)
    
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

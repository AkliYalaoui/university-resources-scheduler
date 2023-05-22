from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import student_required, teacher_required
from .models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant
from .forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm

CustomUser = get_user_model()


@login_required
def home_view(request):
    print(request.user)
    home_context = {
        "user": request.user
    }
    return render(request=request, template_name="home.html", context=home_context)

@login_required
def programs_view(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            return redirect('program_detail', pk=program.pk)  # Replace 'program_detail' with the actual URL name for the program detail view
    else:
        form = ProgramForm()

    return render(request, 'programs.html', {'form': form})


@login_required
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
        return render(request=request, template_name="students.html", context=students_context)


@login_required
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
        return render(request=request, template_name="teachers.html", context=teachers_context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request=request, template_name="login.html")


def logout_view(request):
    logout(request)
    return redirect('login')

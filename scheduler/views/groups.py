from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator


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
        return render(request=request, template_name="groups/home.html", context=groups_context)


@login_required
@admin_required
def group_details_view(request, group_id):
    group = get_object_or_404(Groupe, id=group_id)
    times = ['08:00', '09:30', '11:00', '12:30',
             '14:00', '15:30', '17:00', '18:30']
    days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']

    if request.method == 'POST' and request.POST["_method"] == "delete":
        group.delete()
        return redirect('groups')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        section_id = request.POST['section']

        group.name = name
        group.section = Section.objects.get(id=section_id)

        group.save()
        return redirect('group_details', group_id=group_id)
    elif request.method == 'POST' and request.POST["_method"] == "post":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_details', group_id=group_id)
    elif request.method == 'GET':
        selected_semester_id = request.GET.get('semester')
        selected_semester = None
        if selected_semester_id:
            selected_semester = Semestre.objects.get(id=selected_semester_id)
        semesters = Semestre.objects.all()
        salles = Salle.objects.all()
        modules = Module.objects.filter(
            formation=group.section.formation, semester=selected_semester)
        teachers = Enseignant.objects.all()
        programs = Seance.objects.filter(
            groupe=group, semester=selected_semester)
        sections = Section.objects.all()
        group_context = {
            'group': group,
            'sections': sections,
            "times": times,
            "days": days,
            "salles": salles,
            "modules": modules,
            "teachers": teachers,
            "semesters": semesters,
            "selected_semester": selected_semester,
            'programs': programs
        }
        return render(request=request, template_name="groups/details.html", context=group_context)

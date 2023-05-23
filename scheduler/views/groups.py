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
        return render(request=request, template_name="groups.html", context=groups_context)
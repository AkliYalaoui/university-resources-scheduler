from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator

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
        return render(request=request, template_name="sections/home.html", context=formations_context)
    

@login_required
@admin_required
def section_details_view(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        section.delete()
        return redirect('sections')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        formation_id = request.POST['formation']

        section.name = name
        section.formation = Formation.objects.get(id=formation_id)

        section.save()
        return redirect('section_details', section_id=section_id)
    elif request.method == 'GET':
        formations = Formation.objects.all()
        section_context = {
            'section': section,
            'formations': formations,
        }
        return render(request=request, template_name="sections/details.html", context=section_context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator

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
        paginator = Paginator(formations, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        formations_context = {
            "page_obj": page_obj
        }
        return render(request=request, template_name="formations/home.html", context=formations_context)
    

@login_required
@admin_required
def formation_details_view(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        formation.delete()
        return redirect('formations')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        niveau = request.POST['niveau']
        nb_semestre = request.POST['nb_semestre']

        formation.name = name
        formation.niveau = niveau
        formation.nb_semestre = nb_semestre
        formation.save()
        return redirect('formation_details', formation_id=formation_id)
    elif request.method == 'GET':
        formation_context = {
            'formation': formation,
        }
        return render(request=request, template_name="formations/details.html", context=formation_context)
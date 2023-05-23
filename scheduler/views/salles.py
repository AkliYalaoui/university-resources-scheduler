from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator


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
        paginator = Paginator(salles, 20)
        page_number = request.GET.get('page')
        salles = paginator.get_page(page_number)
        salles_context = {
            "salles": salles
        }
        return render(request=request, template_name="salles/home.html", context=salles_context)
    

@login_required
@admin_required
def salle_details_view(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        salle.delete()
        return redirect('salles')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        type = request.POST['type']
        capacity = request.POST['capacity']

        salle.name = name
        salle.type = type
        salle.capacity = capacity
        salle.save()
        return redirect('salle_details', salle_id=salle_id)
    elif request.method == 'GET':
        salle_context = {
            'salle': salle,
        }
        return render(request=request, template_name="salles/details.html", context=salle_context)
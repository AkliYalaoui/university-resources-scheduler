from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator

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
        formations = Formation.objects.all()
        semesters = Semestre.objects.all()
        modules = Module.objects.all()

        paginator = Paginator(modules, 20)
        page_number = request.GET.get('page')
        modules = paginator.get_page(page_number)

        modules_context = {
            'formations': formations,
            'semesters': semesters,
            'modules': modules,
        }
        return render(request=request, template_name="modules/home.html", context=modules_context)


@login_required
@admin_required
def module_details_view(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        module.delete()
        return redirect('modules')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        volume = request.POST['volume']
        semester_id = request.POST['semester']
        formation_id = request.POST['formation']

        module.name = name
        module.volume = volume
        module.semester = Semestre.objects.get(id=semester_id)
        module.formation = Formation.objects.get(id=formation_id)

        module.save()
        return redirect('module_details', module_id=module_id)
    elif request.method == 'GET':
        formations = Formation.objects.all()
        semesters = Semestre.objects.all()
        module_context = {
            'module': module,
            'formations': formations,
            'semesters': semesters,
        }
        return render(request=request, template_name="modules/details.html", context=module_context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator

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

        paginator = Paginator(semesters, 20)
        page_number = request.GET.get('page')
        semesters = paginator.get_page(page_number)

        semesters_context = {
            "semesters": semesters
        }
        return render(request=request, template_name="semesters/home.html", context=semesters_context)
    

@login_required
@admin_required
def semester_details_view(request, semester_id):
    semester = get_object_or_404(Semestre, id=semester_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        semester.delete()
        return redirect('semesters')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        start = request.POST['start']
        end = request.POST['end']

        semester.name = name
        semester.start = start
        semester.end = end
        semester.save()
        return redirect('semester_details', semester_id=semester_id)
    elif request.method == 'GET':
        semester_context = {
            'semester': semester,
        }
        return render(request=request, template_name="semesters/details.html", context=semester_context)

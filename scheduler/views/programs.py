from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator

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
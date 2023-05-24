import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required, teacher_required
from ..models import Etudiant, Formation, Section, Groupe, Semestre, Salle, Module, Enseignant, Seance
from ..forms import FormationForm, SectionForm, GroupForm, SemestreForm, SalleForm, ModuleForm, ProgramForm
from django.core.paginator import Paginator
from django.db.models import Count


CustomUser = get_user_model()


@login_required
@admin_required
def home_view(request):
    student_count = Etudiant.objects.count()
    teacher_count = Enseignant.objects.count()
    admin_count = CustomUser.objects.filter(is_superuser=True).count()

    formation_student_counts = Formation.objects.annotate(
        student_count=Count('section__groupe__etudiant')).order_by('-student_count')
    formation_data = [
        {'name': formation.name, 'student_count': formation.student_count}
        for formation in formation_student_counts
    ]

    home_context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'admin_count': admin_count,
        'formation_data': json.dumps(formation_data)
    }
    return render(request=request, template_name="home.html", context=home_context)

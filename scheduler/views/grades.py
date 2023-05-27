from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Grade, Enseignant
from ..forms import GradeForm
from django.core.paginator import Paginator


@login_required
@admin_required
def grades_view(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades')

    else:
        grades = Grade.objects.all()
        paginator = Paginator(grades, 20)
        page_number = request.GET.get('page')
        grades = paginator.get_page(page_number)
        grades_context = {
            "grades": grades,
        }
        return render(request=request, template_name="grades/home.html", context=grades_context)


@login_required
@admin_required
def grade_details_view(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        grade.delete()
        return redirect('grades')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        grade.name = name
        grade.save()
        return redirect('grade_details', grade_id=grade_id)
    elif request.method == 'GET':
        grade_count = Enseignant.objects.filter(grade=grade).count()
        teachers = Enseignant.objects.filter(grade=grade)
        paginator = Paginator(teachers, 20)
        page_number = request.GET.get('page')
        teachers = paginator.get_page(page_number)    
        grade_context = {
            'grade': grade,
            'grade_count': grade_count,
            "teachers": teachers
        }
        return render(request=request, template_name="grades/details.html", context=grade_context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import  Semestre
from ..forms import  SemestreForm
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
        sessions = ["février", "juin"]
        paginator = Paginator(semesters, 20)
        page_number = request.GET.get('page')
        semesters = paginator.get_page(page_number)

        semesters_context = {
            "semesters": semesters,
            "sessions": sessions
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
        session = request.POST['session']

        semester.name = name
        semester.start = start
        semester.end = end
        semester.session = session
        semester.save()
        return redirect('semester_details', semester_id=semester_id)
    elif request.method == 'GET':
        sessions = ["février", "juin"]
        semester_context = {
            'semester': semester,
            "sessions": sessions
        }
        return render(request=request, template_name="semesters/details.html", context=semester_context)

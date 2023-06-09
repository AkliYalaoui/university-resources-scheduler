from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, student_required
from ..models import Etudiant,Groupe, Semestre, Seance, Formation, Section
from django.core.paginator import Paginator
from django.urls import reverse
import datetime

CustomUser = get_user_model()

start_times = [datetime.time(8, 00),
               datetime.time(9, 40),
               datetime.time(11, 20),
               datetime.time(13, 00),
               datetime.time(14, 40),
               datetime.time(16, 20)]

days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
labels = ['08:00 - 09:30', '09:40 - 11:10', '11:20 - 12:50', '13:00 - 14:30', '14:40 - 16:10', '16:20 - 17:50']

@login_required
@student_required
def students_search_view(request):
    try:
        formations = Formation.objects.all()
        semesters = Semestre.objects.all()
        error = request.GET.get('error')

        selected_semester_id = request.GET.get('semester')
        selected_formation_id = request.GET.get('formation')
        selected_formation = None
        selected_semester = None
        if selected_formation_id:
            selected_formation = Formation.objects.get(id=selected_formation_id)
            if not selected_formation :
                raise Exception("Formation is required")
        if selected_semester_id:
            selected_semester = Semestre.objects.get(id=selected_semester_id)
            if not selected_semester :
                raise Exception("Semestre is required")

        schedules = []
        if selected_formation and selected_semester:
            seances = Seance.objects.filter(
            groupe__section__formation=selected_formation, semester=selected_semester).order_by('start_time')
            all_sections = Section.objects.filter(formation=selected_formation)

            for section in all_sections:
                all_groups = Groupe.objects.filter(section=section)

                groups = []
                for groupe in all_groups:
                    dimanche = seances.filter(day="dimanche", groupe=groupe)
                    lundi = seances.filter(day="lundi", groupe=groupe)
                    mardi = seances.filter(day="mardi", groupe=groupe)
                    mercredi = seances.filter(day="mercredi", groupe=groupe)
                    jeudi = seances.filter(day="jeudi", groupe=groupe)

                    
                    list_dimanche = []
                    for start_time in start_times:
                        append_time = True
                        for seance in dimanche : 
                            if start_time == seance.start_time :
                                list_dimanche.append(seance)
                                append_time = False
                                break
                        if append_time : 
                            list_dimanche.append({"empty": True})

                    list_lundi = []
                    for start_time in start_times:
                        append_time = True
                        for seance in lundi : 
                            if start_time == seance.start_time :
                                list_lundi.append(seance)
                                append_time = False
                                break
                        if append_time : 
                            list_lundi.append({"empty": True})
                    list_mardi = []
                    for start_time in start_times:
                        append_time = True
                        for seance in mardi : 
                            if start_time == seance.start_time :
                                list_mardi.append(seance)
                                append_time = False
                                break
                        if append_time : 
                            list_mardi.append({"empty": True})
                    list_mercredi = []
                    for start_time in start_times:
                        append_time = True
                        for seance in mercredi : 
                            if start_time == seance.start_time :
                                list_mercredi.append(seance)
                                append_time = False
                                break
                        if append_time : 
                            list_mercredi.append({"empty": True})
                    list_jeudi = []
                    for start_time in start_times:
                        append_time = True
                        for seance in jeudi : 
                            if start_time == seance.start_time :
                                list_jeudi.append(seance)
                                append_time = False
                                break
                        if append_time : 
                            list_jeudi.append({"empty": True})
                    
                    groups.append( {
                        "id" : groupe.pk,
                        "name" : groupe.name,
                        "dimanche" :list_dimanche,
                        "lundi" :list_lundi,
                        "mardi" :list_mardi,
                        "mercredi" :list_mercredi,
                        "jeudi" :list_jeudi,
                    })
                
                schedules.append({
                    "section" : section,
                    "groups" : groups
                })
        
        students_context = {
            "formations": formations,
            "semesters": semesters,
            "selected_formation": selected_formation,
            "selected_semester": selected_semester,
            "schedules": schedules,
            "error" : error,
            "days": days,
            "labels": labels,
        }
        return render(request=request, template_name="students/search.html", context=students_context)
    except Exception as e:
        print(e)
        return redirect(reverse('students_search') + '?error=An+error+occurred+while+getting+the+EDT')

@login_required
@student_required
def students_home_view(request):
    student = get_object_or_404(Etudiant, user_id=request.user.id)
    group = student.groupe
    selected_semester_id = request.GET.get('semester')
    selected_semester = None
    if selected_semester_id:
        selected_semester = Semestre.objects.get(id=selected_semester_id)
    semesters = Semestre.objects.all()
    seances = Seance.objects.filter(
        groupe=group, semester=selected_semester).order_by('start_time')

    dimanche = seances.filter(day="dimanche")
    lundi = seances.filter(day="lundi")
    mardi = seances.filter(day="mardi")
    mercredi = seances.filter(day="mercredi")
    jeudi = seances.filter(day="jeudi")

    list_dimanche = []
    for start_time in start_times:
        append_time = True
        for seance in dimanche : 
            if start_time == seance.start_time :
                list_dimanche.append(seance)
                append_time = False
                break
        if append_time : 
            list_dimanche.append({"empty": True})

    list_lundi = []
    for start_time in start_times:
        append_time = True
        for seance in lundi : 
            if start_time == seance.start_time :
                list_lundi.append(seance)
                append_time = False
                break
        if append_time : 
            list_lundi.append({"empty": True})
    list_mardi = []
    for start_time in start_times:
        append_time = True
        for seance in mardi : 
            if start_time == seance.start_time :
                list_mardi.append(seance)
                append_time = False
                break
        if append_time : 
            list_mardi.append({"empty": True})
    list_mercredi = []
    for start_time in start_times:
        append_time = True
        for seance in mercredi : 
            if start_time == seance.start_time :
                list_mercredi.append(seance)
                append_time = False
                break
        if append_time : 
            list_mercredi.append({"empty": True})
    list_jeudi = []
    for start_time in start_times:
        append_time = True
        for seance in jeudi : 
            if start_time == seance.start_time :
                list_jeudi.append(seance)
                append_time = False
                break
        if append_time : 
            list_jeudi.append({"empty": True})

    students_context = {
        "student": student,
        "days": days,
        "labels": labels,
        "semesters": semesters,
        "selected_semester": selected_semester,
        'dimanche': list_dimanche,
        'lundi': list_lundi,
        'mardi': list_mardi,
        'mercredi': list_mercredi,
        'jeudi': list_jeudi,
    }
    return render(request=request, template_name="students/workspace.html", context=students_context)


@login_required
@admin_required
def students_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type='student')

            selected_group_id = request.POST.get('group')
            selected_group = Groupe.objects.get(id=selected_group_id)

            etudiant = Etudiant.objects.create(user=user, groupe=selected_group)
            return redirect('students')
        except Exception as e:
            print(e)
            return redirect(reverse('students') + '?error=An+error+occurred+while+creating+the+profile')

    else:
        error = request.GET.get('error')
        groups = Groupe.objects.all()
        students = Etudiant.objects.all()

        paginator = Paginator(students, 20)
        page_number = request.GET.get('page')
        students = paginator.get_page(page_number)

        students_context = {
            'groups': groups,
            'students': students,
            'error': error,
        }
        return render(request=request, template_name="students/home.html", context=students_context)


@login_required
@admin_required
def student_details_view(request, student_id):
    student = get_object_or_404(Etudiant, user_id=student_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        student.delete()
        return redirect('students')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            username = request.POST['username']
            group_id = request.POST['group']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            student.user.username = username
            student.user.first_name = first_name
            student.user.last_name = last_name
            student.user.email = email
            student.user.save()

            student.groupe_id = group_id
            student.save()
            return redirect('student_details', student_id=student_id)
        except Exception as e:
            print(e)
            return redirect(reverse('student_details',args=[student_id]) + '?error=An+error+occurred+while+updating+the+profile')
    elif request.method == 'GET':
        groups = Groupe.objects.all()
        error = request.GET.get('error')
        student_context = {
            'student': student,
            "groups": groups,
            "error": error,
        }
        return render(request=request, template_name="students/details.html", context=student_context)

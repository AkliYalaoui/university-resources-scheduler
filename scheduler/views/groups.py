from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Section, Groupe, Semestre, Salle, Module, Enseignant, Seance, Etudiant
from ..forms import GroupForm, ProgramForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import operator
from functools import reduce


@login_required
@admin_required
def groups_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        print(form)
        if form.is_valid():
            selected_section_id = request.POST.get('section')
            selected_section = Section.objects.get(id=selected_section_id)
            form.instance.section = selected_section
            form.save()
            return redirect('groups')

    else:
        sections = Section.objects.all()
        groups = Groupe.objects.all()

        paginator = Paginator(groups, 20)
        page_number = request.GET.get('page')
        groups = paginator.get_page(page_number)

        groups_context = {
            'sections': sections,
            'groups': groups,
        }
        return render(request=request, template_name="groups/home.html", context=groups_context)


@login_required
@admin_required
def group_details_view(request, group_id):
    group = get_object_or_404(Groupe, id=group_id)
    days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']

    if request.method == 'POST' and request.POST["_method"] == "delete":
        group.delete()
        return redirect('groups')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        section_id = request.POST['section']

        group.name = name
        group.section = Section.objects.get(id=section_id)

        group.save()
        return redirect('group_details', group_id=group_id)
    elif request.method == 'POST' and request.POST["_method"] == "post":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_details', group_id=group_id)
    elif request.method == 'POST' and request.POST["_method"] == "patch":
        seance_id = request.POST["seance"]
        seance = get_object_or_404(Seance, id=seance_id)
        seance.delete()
        return redirect('group_details', group_id=group_id)
    elif request.method == 'GET':
        selected_semester_id = request.GET.get('semester')
        selected_semester = None
        if selected_semester_id:
            selected_semester = Semestre.objects.get(id=selected_semester_id)
        semesters = Semestre.objects.all()
        salles = Salle.objects.all()
        modules = Module.objects.filter(
            formation=group.section.formation, semester=selected_semester)
        teachers = Enseignant.objects.all()
        seances = Seance.objects.filter(
            groupe=group, semester=selected_semester).order_by('start_time')

        types = ["td", "tp", "cours"]
        dimanche = seances.filter(day="dimanche")
        lundi = seances.filter(day="lundi")
        mardi = seances.filter(day="mardi")
        mercredi = seances.filter(day="mercredi")
        jeudi = seances.filter(day="jeudi")

        group_context = {
            'group': group,
            "days": days,
            "salles": salles,
            "modules": modules,
            "teachers": teachers,
            "semesters": semesters,
            "selected_semester": selected_semester,
            "types": types,
            'dimanche': dimanche,
            'lundi': lundi,
            'mardi': mardi,
            'mercredi': mercredi,
            'jeudi': jeudi,
        }
        return render(request=request, template_name="groups/details.html", context=group_context)


@csrf_exempt
def allowed_sessions_view(request, group_id, semester_id):
    group = get_object_or_404(Groupe, id=group_id)
    semester = get_object_or_404(Semestre, id=semester_id)

    filtered_modules = []
    if "get_modules" in request.GET:
        # Retrieve the modules that do not exceed their max_weekly_volume
        modules = Module.objects.filter(
            formation=group.section.formation, semester=semester).prefetch_related('seance_set')
        
        for module in modules:
            total_volume = datetime.timedelta()
            for seance in module.seance_set.all():
                start_time = datetime.datetime.combine(
                    datetime.date.today(), seance.start_time)
                end_time = datetime.datetime.combine(
                    datetime.date.today(), seance.end_time)
                duration = end_time - start_time
                total_volume += duration

            if total_volume <= datetime.timedelta(hours=module.weekly_volume):
                filtered_modules.append(module)

    filtered_teachers = []
    if "get_teachers" in request.GET:
        module_id = request.GET["module"]
        module = Module.objects.get(id=module_id)
        teachers = Enseignant.objects.exclude(
            Q(seance__day=request.GET["day"]) & Q(seance__start_time__lte=request.GET["end_time"]) & Q(
                seance__end_time__gte=request.GET["start_time"])
        ).filter(modules=module)

        filtered_teachers = []
        for teacher in teachers:
            total_daily_load = datetime.timedelta()
            for seance in teacher.seance_set.all():
                seance_start = datetime.datetime.combine(datetime.datetime.now().date(), seance.start_time)
                seance_end = datetime.datetime.combine(datetime.datetime.now().date(), seance.end_time)
                duration = seance_end - seance_start
                total_daily_load += duration

            if total_daily_load.total_seconds() / 3600 < teacher.daily_load:
                filtered_teachers.append(teacher)

    seance_types = []
    if "get_types" in request.GET:
        conflicting_sessions = Seance.objects.filter(day=request.GET["day"], start_time__lte=request.GET["end_time"],
                                                     end_time__gte=request.GET["start_time"], type__in=["td", "tp"],  groupe__section=group.section)
        
        print(conflicting_sessions)
        if conflicting_sessions.exists():
            seance_types = ["td", "tp"]
        else : 
            seance_types = ["td", "tp", "cours"]

        conflicting_sessions = Seance.objects.filter(day=request.GET["day"], start_time__lte=request.GET["end_time"],
                                                     end_time__gte=request.GET["start_time"], type__in=["cours"],  groupe__section=group.section)
        if conflicting_sessions.exists():
            seance_types = ["cours"]
        else:
            seance_types = ["td", "tp", "cours"]

    filtered_salles = []
    if "get_rooms" in request.GET:
        occupied_salle_ids = Seance.objects.filter(
            day=request.GET["day"],
            start_time__lte=request.GET["end_time"],
            end_time__gte=request.GET["start_time"]
        ).values_list('salle_id', flat=True)

        # Retrieve the free salles at the target time
        types = {
            "td": ["td", "amphitheater"],
            "cours": ["td", "amphitheater"],
            "tp": ["tp"],
        }

        allowed_types = types.get(request.GET["type"], [])

        if request.GET["type"] in ['td', 'tp']:
            students_count = Etudiant.objects.filter(
                groupe_id=group_id).count()
        else:
            students_count = Etudiant.objects.filter(
                groupe__section_id=group.section.id).count()

        salles = Salle.objects.exclude(id__in=occupied_salle_ids).\
            filter(capacity__gte=students_count)
        print("salles", salles)

        filtered_salles = [
            salle for salle in salles if salle.type in allowed_types
        ]

    modules_data = [{"value": module.id, "label": module.name}
                    for module in filtered_modules]
    teachers_data = [{"value": teacher.user.id, "label": teacher.user.first_name + " " + teacher.user.last_name}
                     for teacher in filtered_teachers]
    types_data = [{"value": type_data, "label": type_data}
                    for type_data in seance_types]
    
    salles_data = [{"value": salle.id, "label": salle.name + "( " + salle.type +" )"}
                    for salle in filtered_salles]
    
    return JsonResponse({"modules": modules_data, "teachers": teachers_data, "types": types_data, "salles": salles_data})

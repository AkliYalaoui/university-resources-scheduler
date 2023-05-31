from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Section, Groupe, Semestre, Salle, Module, Enseignant, Seance, Etudiant
from ..forms import GroupForm, ProgramForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.urls import reverse


start_times = [datetime.time(8, 00),
               datetime.time(9, 40),
               datetime.time(11, 20),
               datetime.time(13, 00),
               datetime.time(14, 40),
               datetime.time(16, 20)]

all_times = [{
    "value": 1,
    "label": "08:00 - 09:30",
    "start_time_ob": datetime.time(8, 00),
    "end_time_ob": datetime.time(9, 30),
},
    {
    "value": 2,
    "label": "09:40 - 11:10",
    "start_time_ob": datetime.time(9, 40),
    "end_time_ob": datetime.time(11, 10),
},
    {
    "value": 3,
    "label": "11:20 - 12:50",
    "start_time_ob": datetime.time(11, 20),
    "end_time_ob": datetime.time(12, 50),
},
    {
    "value": 4,
    "label": "13:00 - 14:30",
    "start_time_ob": datetime.time(13, 00),
    "end_time_ob": datetime.time(14, 30),
},
    {
    "value": 5,
    "label": "14:40 - 16:10",
    "start_time_ob": datetime.time(14, 40),
    "end_time_ob": datetime.time(16, 10),
},
    {
    "value": 6,
    "label": "16:20 - 17:50",
    "start_time_ob": datetime.time(16, 20),
    "end_time_ob": datetime.time(17, 50),
},
]


@login_required
@admin_required
def groups_view(request):
    if request.method == 'POST':
        try:
            form = GroupForm(request.POST)
            print(form)
            if form.is_valid():
                selected_section_id = request.POST.get('section')
                selected_section = Section.objects.get(id=selected_section_id)
                form.instance.section = selected_section
                group = form.save()

                related_sessions = Seance.objects.filter(
                    type="cours", groupe__section=selected_section)
                for cours in related_sessions:
                    new_seance = Seance.objects.create(
                        enseignant=cours.enseignant,
                        subject=cours.subject,
                        groupe=group,
                        semester=cours.semester,
                        salle=cours.salle,
                        day=cours.day,
                        start_time=cours.start_time,
                        end_time=cours.end_time,
                        type=cours.type
                    )

                    print(new_seance)

                return redirect('groups')
            else:
                raise Exception("form not valid")
        except Exception as e:
            print(e)
            return redirect(reverse('groups') + '?error=An+error+occurred+while+creating+the+group')

    else:
        error = request.GET.get('error')
        sections = Section.objects.all()
        groups = Groupe.objects.all()

        paginator = Paginator(groups, 20)
        page_number = request.GET.get('page')
        groups = paginator.get_page(page_number)

        groups_context = {
            'sections': sections,
            'groups': groups,
            'error': error,
        }
        return render(request=request, template_name="groups/home.html", context=groups_context)


@login_required
@admin_required
def group_details_view(request, group_id):
    group = get_object_or_404(Groupe, id=group_id)
    days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
    labels = ['08:00 - 09:30', '09:40 - 11:10', '11:20 - 12:50', '13:00 - 14:30', '14:40 - 16:10', '16:20 - 17:50']

    if request.method == 'POST' and request.POST["_method"] == "delete":
        group.delete()
        return redirect('groups')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            name = request.POST['name']
            section_id = request.POST['section']

            group.name = name
            group.section = Section.objects.get(id=section_id)

            group.save()
            return redirect('group_details', group_id=group_id)
        except Exception as e:
            print(e)
            return redirect(reverse('group_details', args=[group_id]) + '?error=An+error+occurred+while+updating+the+group')

    elif request.method == 'POST' and request.POST["_method"] == "post":
        try:
            modified_post = request.POST.copy()
            time_id = request.POST["creaneau"]
            start_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("start_time_ob")
            end_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("end_time_ob")
            modified_post["start_time"] = start_time
            modified_post["end_time"] = end_time

            form = ProgramForm(modified_post)
            semester_id = request.POST.get('semester')
            if form.is_valid():
                seance = form.save(commit=False)
                seance.save()

                if seance.type == 'cours':
                    related_groups = Groupe.objects.filter(
                        section=group.section).exclude(id=group_id)
                    # Add the same session to each related group
                    for related_group in related_groups:
                        new_seance = Seance.objects.create(
                            enseignant=seance.enseignant,
                            subject=seance.subject,
                            groupe=related_group,
                            semester=seance.semester,
                            salle=seance.salle,
                            day=seance.day,
                            start_time=seance.start_time,
                            end_time=seance.end_time,
                            type=seance.type
                        )

                        print(new_seance)
                return redirect(reverse('group_details', args=[group_id]) + f'?semester={semester_id}')
            else:
                raise Exception("form not valid")
        except Exception as e:
            print(e)
            return redirect(reverse('group_details', args=[group_id]) + '?error=An+error+occurred+while+updating+the+schedule')
    elif request.method == 'POST' and request.POST["_method"] == "patch":
        semester_id = request.POST.get('semester')
        seance_id = request.POST["seance"]
        seance = get_object_or_404(Seance, id=seance_id)

        if seance.type == 'cours':
            seance_remove = Seance.objects.filter(
                type=seance.type,
                day=seance.day,
                start_time=seance.start_time,
                end_time=seance.end_time,
                groupe__section=group.section,
                semester=seance.semester,
            )
            seance_remove.delete()
        else:
            seance.delete()
        return redirect(reverse('group_details', args=[group_id]) + f'?semester={semester_id}')
    elif request.method == 'GET':
        error = request.GET.get('error')
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

        # types = ["td", "tp", "cours"]
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
            if append_time : 
                list_dimanche.append({"empty": True})

        list_lundi = []
        for start_time in start_times:
            append_time = True
            for seance in lundi : 
                if start_time == seance.start_time :
                    list_lundi.append(seance)
                    append_time = False
            if append_time : 
                list_lundi.append({"empty": True})
        list_mardi = []
        for start_time in start_times:
            append_time = True
            for seance in mardi : 
                if start_time == seance.start_time :
                    list_mardi.append(seance)
                    append_time = False
            if append_time : 
                list_mardi.append({"empty": True})
        list_mercredi = []
        for start_time in start_times:
            append_time = True
            for seance in mercredi : 
                if start_time == seance.start_time :
                    list_mercredi.append(seance)
                    append_time = False
            if append_time : 
                list_mercredi.append({"empty": True})
        list_jeudi = []
        for start_time in start_times:
            append_time = True
            for seance in jeudi : 
                if start_time == seance.start_time :
                    list_jeudi.append(seance)
                    append_time = False
            if append_time : 
                list_jeudi.append({"empty": True})

        group_context = {
            'group': group,
            "days": days,
            "labels": labels,
            "salles": salles,
            "modules": modules,
            "teachers": teachers,
            "semesters": semesters,
            "selected_semester": selected_semester,
            # "types": types,
            'dimanche': list_dimanche,
            'lundi': list_lundi,
            'mardi': list_mardi,
            'mercredi': list_mercredi,
            'jeudi': list_jeudi,
            'error': error,
        }
        return render(request=request, template_name="groups/details.html", context=group_context)


@csrf_exempt
def allowed_sessions_view(request, group_id, semester_id):
    group = get_object_or_404(Groupe, id=group_id)
    semester = get_object_or_404(Semestre, id=semester_id)

    filtered_times = all_times.copy()
    if "get_times" in request.GET:
        selected_jour = request.GET.get("day")
        jour_sessions = Seance.objects.filter(
            day=selected_jour, semester=semester, groupe=group)
        for seance in jour_sessions:
            filtered_times = list(
                filter(lambda t: t.get("start_time_ob") != seance.start_time, filtered_times))
            
        print(filtered_times)

    filtered_modules = []
    if "get_modules" in request.GET:
        # Retrieve the modules that do not exceed their max_weekly_volume
        modules = Module.objects.filter(
            formation=group.section.formation, semester=semester).prefetch_related('seance_set')

        for module in modules:
            total_volume = datetime.timedelta()
            for seance in module.seance_set.all():
                if seance.groupe_id != group_id:
                    continue

                print(seance.groupe_id)
                start_time = datetime.datetime.combine(
                    datetime.date.today(), seance.start_time)
                end_time = datetime.datetime.combine(
                    datetime.date.today(), seance.end_time)
                duration = end_time - start_time
                total_volume += duration

            print("total_volume", total_volume)
            if total_volume < datetime.timedelta(hours=module.weekly_volume):
                filtered_modules.append(module)

    filtered_teachers = []
    if "get_teachers" in request.GET:
        module_id = request.GET["module"]
        time_id = request.GET["creaneau"]
        end_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("end_time_ob")
        start_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("start_time_ob")
        module = Module.objects.get(id=module_id)
        teachers = Enseignant.objects.exclude(
            Q(seance__day=request.GET["day"]) & Q(seance__start_time__lte=start_time) & Q(
                seance__end_time__gte=start_time)
        ).filter(modules=module)

        filtered_teachers = []
        for teacher in teachers:
            total_daily_load = datetime.timedelta()
            for seance in teacher.seance_set.all():
                seance_start = datetime.datetime.combine(
                    datetime.datetime.now().date(), seance.start_time)
                seance_end = datetime.datetime.combine(
                    datetime.datetime.now().date(), seance.end_time)
                duration = seance_end - seance_start
                total_daily_load += duration

            if total_daily_load.total_seconds() / 3600 < teacher.daily_load:
                filtered_teachers.append(teacher)

    seance_types = []
    if "get_types" in request.GET:
        time_id = request.GET["creaneau"]
        end_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("end_time_ob")
        start_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("start_time_ob")
        conflicting_sessions = Seance.objects.filter(day=request.GET["day"], start_time__lt=end_time,
                                                     end_time__gt=start_time,  groupe__section=group.section)

        for conflicting_session in conflicting_sessions:
            if conflicting_session.type in ["cours"]:
                seance_types = ["cours"]
                break
            elif conflicting_session.type in ["td", "tp"]:
                seance_types = ["td", "tp"]
                break

        if len(seance_types) == 0:
            seance_types = ["td", "tp", "cours"]

    filtered_salles = []
    if "get_rooms" in request.GET:
        time_id = request.GET["creaneau"]
        end_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("end_time_ob")
        start_time = list(filter(lambda item: item["value"] == int(time_id), all_times))[0].get("start_time_ob")
        occupied_salle_ids = Seance.objects.filter(
            day=request.GET["day"],
            start_time__lte=end_time,
            end_time__gte=start_time
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

    filtered_times = list(map(lambda t: {
                              "value": t.get("value"), "label": t.get("label")}, filtered_times))

    modules_data = [{"value": module.id, "label": module.name}
                    for module in filtered_modules]
    teachers_data = [{"value": teacher.user.id, "label": teacher.user.first_name + " " + teacher.user.last_name}
                     for teacher in filtered_teachers]
    types_data = [{"value": type_data, "label": type_data}
                  for type_data in seance_types]

    salles_data = [{"value": salle.id, "label": salle.name + "( " + salle.type + " )"}
                   for salle in filtered_salles]

    return JsonResponse({"modules": modules_data, "teachers": teachers_data, "types": types_data, "salles": salles_data, "times": filtered_times})

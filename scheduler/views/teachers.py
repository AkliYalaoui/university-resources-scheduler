from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, teacher_required
from ..models import Semestre, Module, Enseignant, Seance
from django.core.paginator import Paginator
from django.urls import reverse
import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from .emails import send_password_create_email, send_password_update_email
from django.db.models import Q


CustomUser = get_user_model()


start_times = [datetime.time(8, 00),
               datetime.time(9, 40),
               datetime.time(11, 20),
               datetime.time(13, 00),
               datetime.time(14, 40),
               datetime.time(16, 20)]


@login_required
@teacher_required
def teachers_suggest_view(request):
    query = request.POST.get('query', '')
    teachers = Enseignant.objects.filter(user__first_name__icontains=query) | Enseignant.objects.filter(user__last_name__icontains=query)
    suggestions = [{"id": teacher.user.id, "full_name": teacher.user.first_name +
                    " " + teacher.user.last_name} for teacher in teachers[:5]]
    print(suggestions)
    # teachers_json = serialize('json', teachers)
    return JsonResponse({'suggestions': suggestions})


@login_required
@teacher_required
def teachers_search_view(request):

    teacher_id = request.GET.get("teacher_id")
    if teacher_id:
        days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
        labels = ['08:00 - 09:30', '09:40 - 11:10', '11:20 - 12:50',
                  '13:00 - 14:30', '14:40 - 16:10', '16:20 - 17:50']

        teacher = get_object_or_404(Enseignant, user_id=teacher_id)
        seances = Seance.objects.filter(
            enseignant=teacher).order_by('start_time')

        semesters = Semestre.objects.all()
        schedules = []
        for semester in semesters:
            dimanche = seances.filter(day="dimanche", semester=semester)
            lundi = seances.filter(day="lundi", semester=semester)
            mardi = seances.filter(day="mardi", semester=semester)
            mercredi = seances.filter(day="mercredi", semester=semester)
            jeudi = seances.filter(day="jeudi", semester=semester)

            list_dimanche = []
            for start_time in start_times:
                append_time = True
                for seance in dimanche:
                    if start_time == seance.start_time:
                        list_dimanche.append(seance)
                        append_time = False
                        break
                if append_time:
                    list_dimanche.append({"empty": True})

            list_lundi = []
            for start_time in start_times:
                append_time = True
                for seance in lundi:
                    if start_time == seance.start_time:
                        list_lundi.append(seance)
                        append_time = False
                        break
                if append_time:
                    list_lundi.append({"empty": True})
            list_mardi = []
            for start_time in start_times:
                append_time = True
                for seance in mardi:
                    if start_time == seance.start_time:
                        list_mardi.append(seance)
                        append_time = False
                        break
                if append_time:
                    list_mardi.append({"empty": True})
            list_mercredi = []
            for start_time in start_times:
                append_time = True
                for seance in mercredi:
                    if start_time == seance.start_time:
                        list_mercredi.append(seance)
                        append_time = False
                        break
                if append_time:
                    list_mercredi.append({"empty": True})
            list_jeudi = []
            for start_time in start_times:
                append_time = True
                for seance in jeudi:
                    if start_time == seance.start_time:
                        list_jeudi.append(seance)
                        append_time = False
                        break
                if append_time:
                    list_jeudi.append({"empty": True})

            schedules.append({
                "semester": semester,
                "dimanche": list_dimanche,
                "lundi": list_lundi,
                "mardi": list_mardi,
                "mercredi": list_mercredi,
                "jeudi": list_jeudi,
            })

        teacher_context = {
            "days": days,
            "labels": labels,
            "schedules": schedules,
            "teacher": teacher
        }
        return render(request=request, template_name="teachers/search.html", context=teacher_context)
    else:
        return render(request=request, template_name="teachers/search.html")


@login_required
@teacher_required
def teachers_home_view(request):
    teacher = get_object_or_404(Enseignant, user_id=request.user.id)
    teacher_modules = teacher.modules.all
    days = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
    labels = ['08:00 - 09:30', '09:40 - 11:10', '11:20 - 12:50',
              '13:00 - 14:30', '14:40 - 16:10', '16:20 - 17:50']

    selected_semester_id = request.GET.get('semester')
    selected_semester = None
    if selected_semester_id:
        selected_semester = Semestre.objects.get(id=selected_semester_id)
    semesters = Semestre.objects.all()
    seances = Seance.objects.filter(
        enseignant=teacher, semester=selected_semester).order_by('start_time')

    dimanche = seances.filter(day="dimanche")
    lundi = seances.filter(day="lundi")
    mardi = seances.filter(day="mardi")
    mercredi = seances.filter(day="mercredi")
    jeudi = seances.filter(day="jeudi")

    list_dimanche = []
    for start_time in start_times:
        append_time = True
        for seance in dimanche:
            if start_time == seance.start_time:
                list_dimanche.append(seance)
                append_time = False
                break
        if append_time:
            list_dimanche.append({"empty": True})

    list_lundi = []
    for start_time in start_times:
        append_time = True
        for seance in lundi:
            if start_time == seance.start_time:
                list_lundi.append(seance)
                append_time = False
                break
        if append_time:
            list_lundi.append({"empty": True})
    list_mardi = []
    for start_time in start_times:
        append_time = True
        for seance in mardi:
            if start_time == seance.start_time:
                list_mardi.append(seance)
                append_time = False
                break
        if append_time:
            list_mardi.append({"empty": True})
    list_mercredi = []
    for start_time in start_times:
        append_time = True
        for seance in mercredi:
            if start_time == seance.start_time:
                list_mercredi.append(seance)
                append_time = False
                break
        if append_time:
            list_mercredi.append({"empty": True})
    list_jeudi = []
    for start_time in start_times:
        append_time = True
        for seance in jeudi:
            if start_time == seance.start_time:
                list_jeudi.append(seance)
                append_time = False
                break
        if append_time:
            list_jeudi.append({"empty": True})

    teacher_context = {
        "teacher": teacher,
        "teacher_modules": teacher_modules,
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
    return render(request=request, template_name="teachers/workspace.html", context=teacher_context)


@login_required
@admin_required
def teachers_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            grade = request.POST['grade']
            daily_load = request.POST['daily_load']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type='teacher')

            teacher = Enseignant.objects.create(
                user=user, grade=grade, daily_load=daily_load)

            send_password_create_email("Enseignant", email, username, password)
            return redirect('teachers')
        except Exception as e:
            print(e)
            return redirect(reverse('teachers') + '?error=An+error+occurred+while+creating+the+profile')

    else:
        error = request.GET.get('error')
        search_query = request.GET.get('search')
        sort_param = request.GET.get('sort')

        teachers = Enseignant.objects.all()

        if search_query:
            teachers = teachers.filter(
                Q(user__username__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(grade__icontains=search_query)
            )
        else:
            search_query = ""

        if sort_param:
            teachers = teachers.order_by(sort_param)
        else:
            teachers = teachers.order_by('user__username')

        paginator = Paginator(teachers, 20)

        page_number = request.GET.get('page')
        teachers = paginator.get_page(page_number)
        teachers_context = {
            'teachers': teachers,
            "search_query": search_query,
            'error': error,
        }
        return render(request=request, template_name="teachers/home.html", context=teachers_context)


@login_required
@admin_required
def teacher_details_view(request, teacher_id):
    teacher = get_object_or_404(Enseignant, user_id=teacher_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        teacher.delete()
        if "_redirect" in request.POST:
            return redirect(request.POST["_redirect"])
        return redirect('teachers')

    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            username = request.POST['username']
            grade = request.POST['grade']
            daily_load = request.POST['daily_load']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']

            teacher.user.username = username
            teacher.user.first_name = first_name
            teacher.user.last_name = last_name
            teacher.user.email = email
            if password:
                teacher.user.set_password(password)
                send_password_update_email(
                    first_name, email, username, password)
            teacher.user.save()

            teacher.grade = grade
            teacher.daily_load = daily_load
            teacher.save()
            return redirect('teachers')
        except Exception as e:
            print(e)
            return redirect(reverse('teachers') + '?error=An+error+occurred+while+updating+the+profile')

    elif request.method == 'POST' and request.POST["_method"] == "post":
        selected_modules = request.POST.getlist("modules")
        teacher.modules.set(selected_modules)
        teacher.save()
        return redirect('teachers')
    elif request.method == 'GET':
        modules = Module.objects.all()
        teacher_modules = teacher.modules.all()
        modules_json = serialize('json', modules)
        teacher_modules_json = serialize('json', teacher_modules)
        return JsonResponse({'modules': modules_json, "teacher_modules": teacher_modules_json})

        # error = request.GET.get('error')
        # modules = Module.objects.all()
        # teacher_modules = teacher.modules.all
        # print(teacher_modules)
        # teacher_context = {
        #     'teacher': teacher,
        #     "teacher_modules": teacher_modules,
        #     "modules": modules,
        #     "error": error,
        # }
        # return render(request=request, template_name="teachers/details.html", context=teacher_context)

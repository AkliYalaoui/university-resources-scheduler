from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required 
from ..models import Formation, Semestre, Module
from ..forms import  ModuleForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Q


@login_required
@admin_required
def modules_view(request):
    if request.method == 'POST':
        try:
            form = ModuleForm(request.POST)
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
                raise Exception("form not valid")
        except Exception as e:
            print(e)
            return redirect(reverse('modules') + '?error=An+error+occurred+while+creating+the+module')

    else:
        error = request.GET.get('error')
        search_query = request.GET.get('search')
        sort_param = request.GET.get('sort')

        formations = Formation.objects.all()
        semesters = Semestre.objects.all()
        modules = Module.objects.all()

        if search_query:
            modules = modules.filter(
                Q(name__icontains=search_query) |
                Q(weekly_volume__icontains=search_query) |
                Q(semester__name__icontains=search_query) |
                Q(formation__name__icontains=search_query) |
                Q(formation__niveau__icontains=search_query) 
            )
        else:
            search_query = ""

        if sort_param:
            modules = modules.order_by(sort_param)
        else:
            modules = modules.order_by('formation__niveau')


        paginator = Paginator(modules, 20)
        page_number = request.GET.get('page')
        modules = paginator.get_page(page_number)

        modules_context = {
            'formations': formations,
            'semesters': semesters,
            'modules': modules,
            'search_query': search_query,
            'error': error,
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
        try:
            name = request.POST['name']
            weekly_volume = request.POST['weekly_volume']
            semester_id = request.POST['semester']
            formation_id = request.POST['formation']

            module.name = name
            module.weekly_volume = weekly_volume
            module.semester = Semestre.objects.get(id=semester_id)
            module.formation = Formation.objects.get(id=formation_id)

            module.save()
            return redirect('modules')
        except Exception as e:
            print(e)
            return redirect(reverse('modules') + '?error=An+error+occurred+while+updating+the+module')
    elif request.method == 'GET':
        formations = Formation.objects.all()
        semesters = Semestre.objects.all()
        formations_json = serialize('json', formations)
        semesters_json = serialize('json', semesters)
        return JsonResponse({'formations': formations_json, "semesters": semesters_json})

        # error = request.GET.get('error')
        # formations = Formation.objects.all()
        # semesters = Semestre.objects.all()
        # module_context = {
        #     'module': module,
        #     'formations': formations,
        #     'semesters': semesters,
        #     'error': error,
        # }
        # return render(request=request, template_name="modules/details.html", context=module_context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Formation, Section
from ..forms import SectionForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q


@login_required
@admin_required
def sections_view(request):
    if request.method == 'POST':
        try:
            form = SectionForm(request.POST)
            if form.is_valid():
                selected_formation_id = request.POST.get('formation')
                selected_formation = Formation.objects.get(
                    id=selected_formation_id)
                form.instance.formation = selected_formation
                form.save()
                return redirect('sections')
            else:
                raise Exception("form not valid")
        except Exception as e:
            print(e)
            return redirect(reverse('sections') + '?error=An+error+occurred+while+creating+the+section')

    else:
        error = request.GET.get('error')
        search_query = request.GET.get('search')
        sort_param = request.GET.get('sort')

        formations = Formation.objects.all()
        sections = Section.objects.all()

        if search_query:
            sections = sections.filter(
                Q(name__icontains=search_query) |
                Q(formation__name__icontains=search_query) |
                Q(formation__niveau__icontains=search_query) 
            )
        else:
            search_query = ""

        if sort_param:
            sections = sections.order_by(sort_param)
        else:
            sections = sections.order_by('formation__niveau')

        paginator = Paginator(sections, 20)
        page_number = request.GET.get('page')
        sections = paginator.get_page(page_number)

        formations_context = {
            'formations': formations,
            'sections': sections,
            'search_query': search_query,
            'error': error,
        }
        return render(request=request, template_name="sections/home.html", context=formations_context)


@login_required
@admin_required
def section_details_view(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        section.delete()
        return redirect('sections')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            name = request.POST['name']
            formation_id = request.POST['formation']

            section.name = name
            section.formation = Formation.objects.get(id=formation_id)

            section.save()
            return redirect('sections')
        except Exception as e:
            print(e)
            return redirect(reverse('sections') + '?error=An+error+occurred+while+updating+the+section')
        
    elif request.method == 'GET':
        formations = Formation.objects.all()
        formations_json = serialize('json', formations)
        return JsonResponse({'formations': formations_json})
        # error = request.GET.get('error')
        # formations = Formation.objects.all()
        # section_context = {
        #     'section': section,
        #     'formations': formations,
        #     'error': error,
        # }
        # return render(request=request, template_name="sections/details.html", context=section_context)

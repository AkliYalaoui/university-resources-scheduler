from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Formation, Section
from ..forms import SectionForm
from django.core.paginator import Paginator
from django.urls import reverse


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
        formations = Formation.objects.all()
        sections = Section.objects.all().order_by('formation__niveau')

        paginator = Paginator(sections, 20)
        page_number = request.GET.get('page')
        sections = paginator.get_page(page_number)

        formations_context = {
            'formations': formations,
            'sections': sections,
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
            return redirect('section_details', section_id=section_id)
        except Exception as e:
            print(e)
            return redirect(reverse('section_details',args=[section_id]) + '?error=An+error+occurred+while+updating+the+section')
        
    elif request.method == 'GET':
        error = request.GET.get('error')
        formations = Formation.objects.all()
        section_context = {
            'section': section,
            'formations': formations,
            'error': error,
        }
        return render(request=request, template_name="sections/details.html", context=section_context)

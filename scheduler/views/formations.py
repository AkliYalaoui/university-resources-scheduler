from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Formation
from ..forms import FormationForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q


@login_required
@admin_required
def formations_view(request):
    if request.method == 'POST':
        try:
            form = FormationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('formations')
            else:
                raise Exception("form not valid")
        except Exception as e:
            print(e)
            return redirect(reverse('formations') + '?error=An+error+occurred+while+creating+the+formation')

    else:
        error = request.GET.get('error')
        search_query = request.GET.get('search')
        sort_param = request.GET.get('sort')

        levels = ["L1", "L2", "L3", "M1", "M2"]
        formations = Formation.objects.all()

        if search_query:
            formations = formations.filter(
                Q(name__icontains=search_query) |
                Q(niveau__icontains=search_query) |
                Q(nb_semestre__icontains=search_query) 
            )
        else:
            search_query = ""

        if sort_param:
            formations = formations.order_by(sort_param)
        else:
            formations = formations.order_by('niveau')
        
        paginator = Paginator(formations, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        formations_context = {
            "page_obj": page_obj,
            "search_query": search_query,
            "levels": levels,
            "error": error,
        }
        return render(request=request, template_name="formations/home.html", context=formations_context)
    

@login_required
@admin_required
def formation_details_view(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        formation.delete()
        return redirect('formations')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            name = request.POST['name']
            niveau = request.POST['niveau']
            nb_semestre = request.POST['nb_semestre']

            formation.name = name
            formation.niveau = niveau
            formation.nb_semestre = nb_semestre
            formation.save()
            return redirect('formations')
        except Exception as e:
            print(e)
            return redirect(reverse('formations') + '?error=An+error+occurred+while+updating+the+formation')
        
    elif request.method == 'GET':
        error = request.GET.get('error')
        levels = ["L1", "L2", "L3", "M1", "M2"]
        formation_context = {
            'formation': formation,
            'levels': levels,
            'error': error,
        }
        return render(request=request, template_name="formations/details.html", context=formation_context)
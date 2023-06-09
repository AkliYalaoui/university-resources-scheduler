from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Salle
from ..forms import SalleForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q


@login_required
@admin_required
def salles_view(request):
    if request.method == 'POST':
        try:
            form = SalleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('salles')
            else:
                raise Exception("form not valid")
        except Exception as e:
            print(e)
            return redirect(reverse('salles') + '?error=An+error+occurred+while+creating+the+salle')

    else:
        error = request.GET.get('error')
        search_query = request.GET.get('search')
        sort_param = request.GET.get('sort')

        salles = Salle.objects.all()
        types = ["td", "tp", "amphitheater"]

        if search_query:
            salles = salles.filter(
                Q(name__icontains=search_query) |
                Q(type__icontains=search_query) |
                Q(capacity__icontains=search_query)
            )
        else:
            search_query = ""

        if sort_param:
            salles = salles.order_by(sort_param)
        else:
            salles = salles.order_by('type')

        paginator = Paginator(salles, 20)
        page_number = request.GET.get('page')
        salles = paginator.get_page(page_number)
        salles_context = {
            "salles": salles,
            "types": types,
            "search_query": search_query,
            "error": error,
        }
        return render(request=request, template_name="salles/home.html", context=salles_context)


@login_required
@admin_required
def salle_details_view(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        salle.delete()
        return redirect('salles')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        try:
            name = request.POST['name']
            type = request.POST['type']
            capacity = request.POST['capacity']

            salle.name = name
            salle.type = type
            salle.capacity = capacity
            salle.save()
            return redirect('salles')
        except Exception as e:
            print(e)
            return redirect(reverse('salles') + '?error=An+error+occurred+while+updating+the+salle')
    elif request.method == 'GET':
        error = request.GET.get('error')
        types = ["td", "tp", "amphitheater"]
        salle_context = {
            'salle': salle,
            'types': types,
            'error': error,
        }
        return render(request=request, template_name="salles/details.html", context=salle_context)

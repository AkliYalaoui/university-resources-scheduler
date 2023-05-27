from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Salle,  TypeSalle
from ..forms import TypeSalleForm
from django.core.paginator import Paginator


@login_required
@admin_required
def type_salles_view(request):
    if request.method == 'POST':
        form = TypeSalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('type_salles')

    else:
        types = TypeSalle.objects.all()
        paginator = Paginator(types, 20)
        page_number = request.GET.get('page')
        types = paginator.get_page(page_number)
        type_salles_context = {
            "types": types,
        }
        return render(request=request, template_name="type_salles/home.html", context=type_salles_context)


@login_required
@admin_required
def type_salle_details_view(request, type_id):
    type_salle = get_object_or_404(TypeSalle, id=type_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        type_salle.delete()
        return redirect('type_salles')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        type_salle.name = name
        type_salle.save()
        return redirect('type_salle_details', type_id=type_id)
    elif request.method == 'GET':
        salle_count = Salle.objects.filter(type=type_salle).count()
        salles = Salle.objects.filter(type=type_salle)
        paginator = Paginator(salles, 20)
        page_number = request.GET.get('page')
        salles = paginator.get_page(page_number)   
        type_salle_context = {
            'type_salle': type_salle,
            'salles': salles,
            'salle_count': salle_count,
        }
        return render(request=request, template_name="type_salles/details.html", context=type_salle_context)

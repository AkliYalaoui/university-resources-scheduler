from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..models import Salle,  TypeSalle
from ..forms import SalleForm
from django.core.paginator import Paginator


@login_required
@admin_required
def salles_view(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            type_id = request.POST['type']
            type = TypeSalle.objects.get(id=type_id)
            form.instance.type = type
            form.save()
            return redirect('salles')

    else:
        salles = Salle.objects.all()
        types = TypeSalle.objects.all()
        paginator = Paginator(salles, 20)
        page_number = request.GET.get('page')
        salles = paginator.get_page(page_number)
        salles_context = {
            "salles": salles,
            "types": types,
        }
        return render(request=request, template_name="salles/home.html", context=salles_context)


@login_required
@admin_required
def salle_details_view(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if request.method == 'POST' and request.POST["_method"] == "delete":
        salle.delete()
        if request.POST["_redirect"]:
            return redirect(request.POST["_redirect"])
        return redirect('salles')
    elif request.method == 'POST' and request.POST["_method"] == "put":
        name = request.POST['name']
        type_id = request.POST['type']
        capacity = request.POST['capacity']

        type = TypeSalle.objects.get(id=type_id)
        salle.name = name
        salle.type = type
        salle.capacity = capacity
        salle.save()
        return redirect('salle_details', salle_id=salle_id)
    elif request.method == 'GET':
        types = TypeSalle.objects.all()
        salle_context = {
            'salle': salle,
            'types': types,
        }
        return render(request=request, template_name="salles/details.html", context=salle_context)

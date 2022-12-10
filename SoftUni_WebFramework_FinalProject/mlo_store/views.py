from django.shortcuts import render
from django.views import generic as views

from SoftUni_WebFramework_FinalProject.mlo_store.models import Item


# Create your views here.


# def index(request):
#     return render(
#         request,
#         'store/index.html',
#     )


class ItemListView(views.ListView):

    model = Item

    template_name = 'store/index.html'


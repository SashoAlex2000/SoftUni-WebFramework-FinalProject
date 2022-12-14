from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic as views

from SoftUni_WebFramework_FinalProject.mlo_store.forms import ItemCreateForm
from SoftUni_WebFramework_FinalProject.mlo_store.models import Item

ITEM_CATEGORIES = {
    'electronics': 'Electronics',
    'apparel': 'Apparel',
    'shoes': 'Shoes',
    'home_and_garden': 'Home and Garden',
    'sports': 'Sports',
    'auto_parts': 'Auto Parts',
    'other': 'Other',

}


# Create your views here.


# def index(request):
#     return render(
#         request,
#         'store/index.html',
#     )


class ItemListView(views.ListView):
    model = Item

    template_name = 'store/index.html'

    extra_context = {
        'categories': [[key, value] for key, value in ITEM_CATEGORIES.items()],
    }

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)

        pattern = self.request.GET.get('pattern', None)
        if pattern:
            data['pattern'] = pattern

        department = self.request.GET.get('department', None)
        if department:
            data["department"] = department

        sorting_param = self.__get_sorting_param()
        if sorting_param:
            data['sorting_param'] = sorting_param

        return data

    def get_queryset(self):
        queryset = super().get_queryset()

        pattern = self.__get_pattern()
        desired_department = self.__get_desired_department()
        sorting_param = self.__get_sorting_param()
        print(sorting_param)

        if not desired_department:
            pass

        else:
            if desired_department == 'all':
                pass
            else:
                print(queryset)
                queryset = queryset.filter(category__icontains=desired_department)
                print(queryset)

        if pattern:
            # queryset = queryset.filter(name__icontains=pattern.lower())
            queryset = queryset.filter(Q(name__icontains=pattern.lower()) | Q(description__icontains=pattern.lower()))
            # queryset = queryset.filter(name__icontains=pattern.lower()).filter(description__icontains=pattern.lower())
            # queryset = queryset.filter(description__icontains=pattern.lower())

        if sorting_param:
            if sorting_param == 'price-asc':
                queryset = queryset.order_by('price')
            elif sorting_param == 'price-desc':
                queryset = queryset.order_by('-price')
            elif sorting_param == 'date-desc':
                queryset = queryset.order_by('-pk')
            elif sorting_param == 'date-asc':
                queryset = queryset.order_by('pk')
        else:
            queryset = queryset.order_by('pk')

        outside_context = pattern

        print(pattern if pattern else 'NONE')
        print(desired_department)
        print(queryset)
        return queryset

    def __get_pattern(self):
        return self.request.GET.get('pattern', None)

    def __get_desired_department(self):
        return self.request.GET.get('department', None)

    def __get_sorting_param(self):
        return self.request.GET.get('sorting', None)


class ItemDetailView(views.DetailView):
    model = Item

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)

        current_ID = self.kwargs['pk']
        current_item = Item.objects.filter(pk=current_ID).get()
        print(current_item.owner.isCompany)
        fee = 1 if current_item.owner.isCompany else 2
        data['fee'] = fee
        print(current_item.price)
        total_price = current_item.price + fee
        data['total_price'] = total_price

        data['can_buy'] = total_price < self.request.user.money
        print(total_price < self.request.user.money)

        return data

    template_name = 'store/details.html'


def buy_item(request, pk):

    print(request.META['HTTP_REFERER'])
    current_item = Item.objects.filter(pk=pk).get()
    current_item.quantity -= 1
    current_item.save()

    cost = current_item.price
    print(cost)

    user_owner = current_item.owner
    user_owner.money += cost
    print(user_owner.money)
    user_owner.save()

    current_user = request.user
    print(current_user)
    current_user.money -= cost
    current_user.save()

    return redirect('details item', pk=pk)


def item_create_view(request):
    if request.method == 'GET':
        form = ItemCreateForm
    else:
        form = ItemCreateForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)

            item.owner = request.user
            item.save()

            return redirect('index')

    context = {
        'form': form,
    }

    return render(
        request,
        'store/create-item.html',
        context
    )

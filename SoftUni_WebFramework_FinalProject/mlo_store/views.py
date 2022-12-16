from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic as views

from SoftUni_WebFramework_FinalProject.mlo_store.forms import ItemCreateForm, UserChargeAccountForm
from SoftUni_WebFramework_FinalProject.mlo_store.models import Item, AccountingBalance

from django.contrib.auth.decorators import user_passes_test

# categories of items in the store, used for filtering
ITEM_CATEGORIES = {
    'electronics': 'Electronics',
    'apparel': 'Apparel',
    'shoes': 'Shoes',
    'home_and_garden': 'Home and Garden',
    'sports': 'Sports',
    'auto_parts': 'Auto Parts',
    'other': 'Other',

}

# getting the AppUser the right way, used in a lot of functions
UserModel = get_user_model()


# function used to calculate the fee based on whether the owner is a company or not
def calculate_fee(price, is_company):
    if is_company:
        fee = 1 if price < 100 else 2 if price < 200 else 2
    else:
        fee = 2 if price < 100 else 3

    return fee


class ItemListView(views.ListView):  # Main page
    model = Item

    template_name = 'store/index.html'

    extra_context = {
        'categories': [[key, value] for key, value in ITEM_CATEGORIES.items()],
    }

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)

        # we pass the various queries in the template to pre-populate, for better UX
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

        # get the different sorting params, if any
        pattern = self.__get_pattern()
        desired_department = self.__get_desired_department()
        sorting_param = self.__get_sorting_param()

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
            # the searching pattern is used, if present, to search in both name and description
            queryset = queryset.filter(Q(name__icontains=pattern.lower()) | Q(description__icontains=pattern.lower()))

        # use the sorting param to sort the filtered queryset
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

        # ???
        outside_context = pattern

        # another property to the object is added - fee; to be displayed in 'index'
        for obj in queryset:
            current_owner = UserModel.objects.filter(pk=obj.owner.pk).get()
            fee = calculate_fee(obj.price, current_owner.isCompany)
            obj.total_price = fee + obj.price

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
        # fee = 1 if current_item.owner.isCompany else 2
        fee = calculate_fee(current_item.price, current_item.owner.isCompany)
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

    item_owner = UserModel.objects.filter(pk=current_item.owner.pk).get()
    fee = calculate_fee(cost, item_owner.isCompany)

    print(item_owner)
    print(fee)

    user_owner = current_item.owner
    user_owner.money += cost
    user_owner.total_money_earned += cost
    print(user_owner.money)
    user_owner.save()

    current_user = request.user
    print(current_user)
    current_user.money -= cost
    current_user.money -= fee
    current_user.total_money_spent += cost
    current_user.total_money_spent += fee
    current_user.save()

    accounting_balance = AccountingBalance.objects.filter(pk=1).get()
    accounting_balance.assets -= cost
    accounting_balance.liabilities -= cost
    accounting_balance.liabilities -= fee
    accounting_balance.equity += fee
    accounting_balance.save()

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


# @user_passes_test(lambda u: u.is_staff)
def charge_account_view(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    users = UserModel.objects.all()
    current_profile_pk = pk
    # print(current_profile_pk)
    # instance = UserModel.objects.filter(pk=pk).get()
    # print(instance)

    if request.method == 'GET':
        form = UserChargeAccountForm()
    else:
        form = UserChargeAccountForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['top_up_amount'])
            topped_up_amount = form.cleaned_data['top_up_amount']
            current_user = UserModel.objects.filter(pk=current_profile_pk).get()
            print(current_user.money)
            # current_user.money += form.cleaned_data['top_up_amount']
            current_user.money += topped_up_amount
            current_user.save()
            accounting_balance = AccountingBalance.objects.filter(pk=1).get()
            accounting_balance.assets += topped_up_amount
            accounting_balance.liabilities += topped_up_amount
            accounting_balance.save()
            print(current_user.money)
            return redirect('profile', pk=pk)

    context = {
        'users': users,
        'form': form,
        'current_profile_pk': current_profile_pk,
    }

    return render(
        request,
        'store/charge-account.html',
        context,
    )


def completed_charging_account(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    context = {
        'curr_user_pk': pk,
    }

    return render(
        request,
        'store/completed-charging.html',
        context,
    )


class AllProfilesListView(views.ListView):
    model = UserModel
    template_name = 'store/all-profiles.html'

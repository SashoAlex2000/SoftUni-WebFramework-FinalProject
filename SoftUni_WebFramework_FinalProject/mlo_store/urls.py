from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from SoftUni_WebFramework_FinalProject.mlo_store.views import ItemListView, ItemDetailView, item_create_view, buy_item, \
    charge_account_view, completed_charging_account, AllProfilesListView, post_comment, post_rating, edit_post_view, \
    general_ledger_view, show_department_view, remove_rating, ItemDeleteView, show_about_view

urlpatterns = [
    path('', ItemListView.as_view(), name='index'),
    path('about/', show_about_view, name='about'),
    path('departments/<slug:department>', show_department_view, name='departments'),
    path('<int:pk>/', ItemDetailView.as_view(), name='details item'),
    path('<int:pk>/edit', edit_post_view, name='edit item'),
    path('<int:pk>/delete', ItemDeleteView.as_view(), name='delete item'),
    path('<int:pk>/post-comment/', post_comment, name='post comment'),
    path('<int:pk>/post-rating/', post_rating, name='post rating'),
    path('<int:pk>/remove-rating/', remove_rating, name='remove rating'),
    path('<int:pk>/buy', buy_item, name='buy item'),
    path('create/', item_create_view, name='create item'),
    path('charge/<int:pk>', charge_account_view, name="charge profile"),
    path('topup/<int:pk>', completed_charging_account, name="completed top up"),
    path('profiles/', AllProfilesListView.as_view(), name="all profiles"),
    path('general-ledger/', general_ledger_view, name="general ledger")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

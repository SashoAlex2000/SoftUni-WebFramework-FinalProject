from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from SoftUni_WebFramework_FinalProject.mlo_store.views import ItemListView, ItemDetailView, item_create_view

urlpatterns = [
    path('', ItemListView.as_view(), name='index'),
    path('<int:pk>/', ItemDetailView.as_view(), name='details item'),
    path('create/', item_create_view, name='create item'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from SoftUni_WebFramework_FinalProject.mlo_store.views import ItemListView

urlpatterns = [
    path('', ItemListView.as_view(), name='index'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

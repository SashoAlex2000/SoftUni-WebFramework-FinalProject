from django.contrib import admin

from SoftUni_WebFramework_FinalProject.mlo_store.models import Item


# Register your models here.


@admin.register(Item)
class StoreAdmin(admin.ModelAdmin):
    pass

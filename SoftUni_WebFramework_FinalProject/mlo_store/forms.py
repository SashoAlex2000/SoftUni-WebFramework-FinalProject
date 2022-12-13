from django import forms

from SoftUni_WebFramework_FinalProject.mlo_store.models import Item


class ItemBaseForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('publication_date', 'owner')

        widgets = {

            'publication_date': forms.DateInput(
                attrs={
                    'placeholder': 'mm/dd/yyyy',
                    'type': 'date',
                }
            ),
        }


class ItemCreateForm(ItemBaseForm):
    pass

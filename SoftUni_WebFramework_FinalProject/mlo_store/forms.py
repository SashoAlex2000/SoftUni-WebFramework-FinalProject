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
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'cols': 15,
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'autofocus': 'off',
                }
            )
        }


class ItemCreateForm(ItemBaseForm):
    pass

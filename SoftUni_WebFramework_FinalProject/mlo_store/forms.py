from enum import Enum

from django import forms
from django.contrib.auth import get_user_model

from SoftUni_WebFramework_FinalProject.mlo_store.models import Item

UserModel = get_user_model()


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


class ItemEditForm(ItemBaseForm):

    class Meta:
        model = Item
        exclude = ('publication_date', 'owner', 'photo')


class UserChargeAccountForm(forms.Form):

    top_up_amount = forms.DecimalField(
        max_digits=9,
        decimal_places=2,
    )


class UserComment(forms.Form):

    COMMENT_MAX_LENGTH = 50

    comment = forms.CharField(
        max_length=COMMENT_MAX_LENGTH,
    )


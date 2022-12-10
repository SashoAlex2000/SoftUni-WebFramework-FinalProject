from django.db import models

# Create your models here.


class Item(models.Model):

    MAX_NAME_LENGTH = 30

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        blank=False,
    )

    description = models.TextField(
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=False,
        null=False,
    )

    publication_date = models.DateField(
        auto_now = True,
        null=False,
        blank=True,
    )

    photo = models.ImageField(
        upload_to='item_photos/',

        blank=False,
        null=False,

    )





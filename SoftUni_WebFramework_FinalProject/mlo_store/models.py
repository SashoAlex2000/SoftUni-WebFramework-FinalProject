from enum import Enum

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators
# Create your models here.

UserModel = get_user_model()


class ChoicesEnumMixin:

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class Categories(ChoicesEnumMixin, Enum):
    electronics = 'Electronics'
    apparel = 'Apparel'
    shoes = 'Shoes'
    home_and_garden = 'Home and Garden'
    sports = 'Sports'
    auto_parts = 'Auto Parts'
    other = 'Other'


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
        auto_now=True,
        null=False,
        blank=True,
    )

    photo = models.ImageField(
        upload_to='item_photos/',

        blank=False,
        null=False,

    )

    category = models.CharField(
        choices=Categories.choices(),
        max_length=Categories.max_len(),
        blank=False,
        null=False,
    )

    quantity = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    # TODO - see why this breaks editing in the ADMIN
    # def save(self, *args, **kwargs):
    #     super().save(self, *args, **kwargs)
    #
    #     img = Image.open(self.photo.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         new_img = (300, 300)
    #         img.thumbnail(new_img)
    #         img.save(self.photo.path)


class AccountingBalance(models.Model):

    assets = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=False,
        null=False,
    )

    liabilities = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=False,
        null=False,
    )

    equity = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=False,
        null=False,
    )


class ItemComment(models.Model):

    MAX_COMMENT_LENGTH = 100

    comment_text = models.CharField(
        max_length=MAX_COMMENT_LENGTH,
        null=False,
        blank=False,
    )

    date_of_publication = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )


class ItemRating(models.Model):

    MIN_RATING = 1
    MAX_RATING = 5

    rating = models.IntegerField(
        validators=(
            validators.MinValueValidator(MIN_RATING),
            validators.MaxValueValidator(MAX_RATING),
        ),
        blank=False,
        null=False,
    )

    date_of_rating = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )


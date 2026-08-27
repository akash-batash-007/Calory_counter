from django.db import models
from django.contrib.auth.models import AbstractUser


class customUser(AbstractUser):

    pass

    def __str__(self):
        return f'{self.username}'

class profileModel(models.Model):

    user = models.ForeignKey(
        customUser,
        on_delete=models.CASCADE,
        null=True,
    )

    GENDER_OPTIONS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    # Name, Age, Gender, Height, Weight
    name = models.CharField(null=True, max_length=200)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(null=True, max_length=100, choices=GENDER_OPTIONS)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    bmr = models.FloatField(null=True)

    def __str__(self):
        return f'{self.name}'


class consumedColorieModel(models.Model):

    consumed_by = models.ForeignKey(
        customUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_calorie'
    )

    item_name = models.CharField(null=True, max_length=200)
    calorie = models.FloatField(null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return {self.item_name}-{self.consumed_by.username}
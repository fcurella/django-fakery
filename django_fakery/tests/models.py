from django.db import models


class Chef(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=4)
    gluten_free = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    chef = models.ForeignKey(Chef)

from decimal import Decimal
from django.db import models


class Chef(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)


class Pizza(models.Model):
    THICKNESSES = (
        (0, 'thin'),
        (1, 'thick'),
        (2, 'deep dish'),
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=4)
    gluten_free = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    thickness = models.CharField(max_length=50, choices=THICKNESSES)
    backed_on = models.DateTimeField()

    chef = models.ForeignKey(Chef)

    def get_price(self, tax):
        return (Decimal('7.99') + (Decimal('7.99') * Decimal(tax))).quantize(Decimal('0.01'))

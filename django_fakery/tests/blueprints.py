from django_fakery.blueprint import Blueprint


chef = Blueprint(
    'tests.Chef',
    fields={
        'first_name': 'Chef %(n)s'
    }
)

pizza = Blueprint(
    'tests.Pizza',
    fields={
        'chef': chef
    }
)

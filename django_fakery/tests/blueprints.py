from django_fakery.blueprint import Blueprint


chef = Blueprint(
    'tests.Chef',
    fields={
        'first_name': 'Chef {}'
    }
)

pizza = Blueprint(
    'tests.Pizza',
    fields={
        'chef': chef
    }
)

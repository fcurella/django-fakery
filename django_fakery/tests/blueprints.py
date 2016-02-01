from django_fakery import factory, Blueprint


chef = factory.blueprint(
    'tests.Chef',
    fields={
        'first_name': 'Chef {}'
    }
)


pizza = Blueprint(
    'tests.Pizza',
    fields={
        'chef': chef,
        'thickness': 1
    }
)

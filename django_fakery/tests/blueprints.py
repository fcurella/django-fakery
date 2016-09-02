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


chef_short = factory.blueprint('tests.Chef').fields(
    first_name='Chef {}',
)

pizza_short = Blueprint('tests.Pizza').fields(
    chef=chef_short,
    thickness=1,
)

__author__ = 'igor'
from catalog.models import Category


def context_data(request):
    return {'nodes': Category.objects.filter(enable=True).all()}

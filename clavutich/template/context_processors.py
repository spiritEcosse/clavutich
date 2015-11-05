__author__ = 'igor'
from catalog.models import Category
from cart import Cart


def context_data(request):
    return {'nodes': Category.objects.filter(enable=True).all()}

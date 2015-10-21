__author__ = 'igor'
from catalog.models import Category


def context_data(request):
    return {'categories': Category.objects.filter(parent=None, enable=1).prefetch_related('categories').iterator()}

__author__ = 'igor'
from django.views.generic.base import TemplateView
from catalog.models import Category


class IndexView(TemplateView):
    template_name = 'base.html'
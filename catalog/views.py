# --coding: utf-8--

import json

from catalog.models import Product, Category
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, Http404
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse
from cart.cart import Cart
from django.views.generic import View
from django.core import serializers


def get_obj(slug, model):
    """
    Get object or 404 from slug
    :return: object Product
    """
    concatenated_slugs = slug
    slugs = concatenated_slugs.split(model._slug_separator)

    try:
        obj = get_object_or_404(model, slug=slugs[-1], enable=True)
    except IndexError:
        raise Http404

    return obj


def redirect_if_necessary(current_path, obj):
    """
    If the slug has changed, issue a redirect.
    :param current_path:
    :param obj:
    :return: redirect if necessary or None
    """
    expected_path = obj.get_absolute_url()
    if expected_path != urlquote(current_path):
        return HttpResponsePermanentRedirect(expected_path)


class CategoryDetailView(SingleObjectMixin, generic.ListView):
    model = Category
    paginate_by = 24
    template_name = 'catalog/category_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Fetch the category; return 404 or redirect as needed
        :param request:
        :param args:
        :param kwargs:
        :return: parent action
        """
        self.object = get_obj(self.kwargs['slug'], Category)
        potential_redirect = redirect_if_necessary(request.path, self.object)

        if potential_redirect is not None:
            return potential_redirect

        self.kwargs['slug'] = self.object.slug
        self.object = self.get_object(queryset=Category.objects.filter(enable=True).all())
        return super(CategoryDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.products.filter(enable=True).all()

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = self.object
        context['categories'] = self.object.get_children().filter(enable=True)
        return context


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class ProductDetailView(JSONResponseMixin, generic.DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data_ajax(self, **kwargs):
        return serializers.serialize('json', self.object)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.render_to_json_response(self.get_context_data_ajax(**kwargs), **kwargs)
        return super(ProductDetailView, self).post(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        Fetch the product; return 404 or redirect as needed
        :param request:
        :param args:
        :param kwargs:
        :return: redirect or parent action
        """
        self.object = get_obj(self.kwargs['slug'], Product)
        potential_redirect = redirect_if_necessary(request.path, self.object)

        if potential_redirect is not None:
            return potential_redirect

        self.kwargs['slug'] = self.object.slug
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['category'] = self.object.category
        return context


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class ProductAddToCart(SingleObjectMixin, JSONResponseMixin, View):
    model = Product

    def post(self, request, *args, **kwargs):
        del kwargs['pk']
        self.object = self.get_object()
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        data = json.loads(self.request.body)
        cart = Cart(self.request)
        cart.add(self.object, 0, data.get('quantity'))
        return {'msg': u'Товар в корзине'}

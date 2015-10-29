# --coding: utf-8--

from django.shortcuts import render
from django.views.generic.base import TemplateView
from cart import Cart
from django.views.generic.base import ContextMixin
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.http import JsonResponse
import json
from catalog.models import Product


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
        from django.core import serializers
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class ShowView(TemplateView, JSONResponseMixin):
    template_name = 'easy_cart/show.html'

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        context = dict()
        context['products'] = [{'pk': product.product.pk, 'quantity': product.quantity} for product in Cart(self.request)]
        return context


class OrderView(TemplateView):
    template_name = 'easy_cart/order.html'


class UpdateQuantityProductView(SingleObjectMixin, JSONResponseMixin, View):
    model = Product

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        self.kwargs['pk'] = data.get('product_pk')
        self.object = self.get_object()
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        data = json.loads(self.request.body)
        cart = Cart(self.request)
        cart.update(self.object, data.get('quantity'), 0)
        return {'msg': u'Количество товара обновлено.'}


class RemoveProduct(SingleObjectMixin, JSONResponseMixin, View):
    model = Product

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        self.kwargs['pk'] = data.get('product_pk')
        self.object = self.get_object()
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        cart.remove(self.object)
        return {'msg': u'Товар удален.'}
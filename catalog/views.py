# --coding: utf-8--

from catalog.models import Product, Category
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, Http404
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse
import json
from cart import Cart
from django.views.generic import View


def get_obj(self):
    # Get object or 404 from slug
    concatenated_slugs = self.kwargs['slug']
    slugs = concatenated_slugs.split(self.model._slug_separator)

    try:
        obj = get_object_or_404(self.model, slug=slugs[-1])
    except IndexError:
        raise Http404

    return obj


def redirect_if_necessary(current_path, obj):
    # If the slug has changed, issue a redirect.
    expected_path = obj.get_absolute_url()
    if expected_path != urlquote(current_path):
        return HttpResponsePermanentRedirect(expected_path)


class CategoryDetailView(SingleObjectMixin, generic.ListView):
    model = Category
    paginate_by = 24
    template_name = 'catalog/category_detail.html'

    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed
        self.category = get_obj(self)
        potential_redirect = redirect_if_necessary(request.path, self.category)

        if potential_redirect is not None:
            return potential_redirect

        self.kwargs['slug'] = self.category.slug
        self.object = self.get_object(queryset=Category.objects.all())
        return super(CategoryDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.products.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = self.object
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get(self, request, *args, **kwargs):
        # Fetch the product; return 404 or redirect as needed
        self.product = get_obj(self)
        potential_redirect = redirect_if_necessary(request.path, self.product)

        if potential_redirect is not None:
            return potential_redirect

        self.kwargs['slug'] = self.product.slug
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
        from django.core import serializers
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class ProductAddToCart(SingleObjectMixin, JSONResponseMixin, View):
    model = Product

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        del kwargs['pk']
        self.object = self.get_object()
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        data = json.loads(self.request.body)
        cart = Cart(self.request)
        cart.add(self.object, 0, data.get('quantity'))
        return {'msg': u'Товар в корзине'}

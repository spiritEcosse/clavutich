from catalog.models import Product, Category
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, Http404
from django.utils.http import urlquote


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
    paginate_by = 1
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


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get(self, request, *args, **kwargs):
        self.product = get_obj(self)
        potential_redirect = redirect_if_necessary(request.path, self.product)

        if potential_redirect is not None:
            return potential_redirect

        self.kwargs['slug'] = self.product.slug
        return super(ProductDetailView, self).get(request, *args, **kwargs)
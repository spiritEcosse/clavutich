from django.shortcuts import render
from catalog.models import Product, Category
from django.views import generic
from django.views.generic.detail import SingleObjectMixin


class CategoryDetailView(SingleObjectMixin, generic.ListView):
    model = Category
    paginate_by = 1
    template_name = 'catalog/category_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super(CategoryDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.products.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['nodes'] = Category.objects.all()
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('product_slug', False):
            self.kwargs['slug'] = self.kwargs['product_slug'].split('/').pop()
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['categories_menu'] = Category.objects.filter(parent=None, enable=1).prefetch_related('categories').iterator()
        return context

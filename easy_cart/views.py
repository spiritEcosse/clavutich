# --coding: utf-8--

import json

from django.views.generic.base import TemplateView
from cart.cart import Cart
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.http import JsonResponse
from catalog.models import Product
from forms import UserDataForm
from djangular.forms import NgModelFormMixin
from django.http import HttpResponse
from clavutich.settings import EMAIL_COMPANY
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from easy_thumbnails.files import get_thumbnailer


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


def get_products(self):
    cart = Cart(self.request)
    products = []
    for product in cart:
        item = dict()
        item['quantity'] = product.quantity
        item['title'] = product.product.title.capitalize()
        item['pk'] = product.product.pk
        item['absolute_url'] = product.product.get_absolute_url()
        options = {'size': (100, 100), 'crop': True}
        item['image_thumb'] = get_thumbnailer(product.product.image).get_thumbnail(options).url
        products.append(item)
    return {'products': products}


class ShowView(TemplateView, JSONResponseMixin):
    template_name = 'easy_cart/show.html'

    def get_context_data_ajax(self, **kwargs):
        return get_products(self)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.render_to_json_response(self.get_context_data_ajax(**kwargs), **kwargs)


class ScopeUserDataForm(NgModelFormMixin, UserDataForm):
    scope_prefix = 'user_data'
    form_name = 'form_user_data'


class OrderView(JSONResponseMixin, FormView):
    template_name = 'easy_cart/order.html'
    form_class = ScopeUserDataForm

    def post(self, request, **kwargs):
        if request.is_ajax():
            return self.ajax(**kwargs)
        return super(OrderView, self).post(request, **kwargs)

    def ajax(self, **kwargs):
        form = self.form_class(data=json.loads(self.request.body))
        response_data = {'errors': form.errors}

        if not form.errors:
            self.send_message(form)
            cart = Cart(self.request)
            cart.clear()
            response_data['msg'] = u'Ваш заказ принят!'

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def send_message(self, form):
        subject = u'Заказ на сайта %s' % self.request.get_host()
        text_content = u'Имя: %s.<br/>' % form.cleaned_data['name']
        text_content += u'Электронная почта: %s.<br/>' % form.cleaned_data['email']
        text_content += u'Номер телефона: %s.<br/>' % form.cleaned_data['phone']

        if form.cleaned_data['comment']:
            text_content += u'Комментарий: %s.<br/>' % form.cleaned_data['comment']

        text_content += '<br/>'
        msg = EmailMultiAlternatives(subject, '', EMAIL_COMPANY, [form.cleaned_data['email'], EMAIL_COMPANY])
        template = get_template('easy_cart/email.html')
        html_content = template.render(get_products(self))
        text_content += html_content
        msg.attach_alternative(text_content, "text/html")
        msg.send()
        msg = EmailMultiAlternatives(subject, '', form.cleaned_data['email'], [EMAIL_COMPANY])
        msg.attach_alternative(text_content, "text/html")
        msg.send()


class UpdateQuantityProductView(SingleObjectMixin, JSONResponseMixin, View):
    model = Product

    def post(self, request, *args, **kwargs):
        del kwargs['pk']
        self.object = self.get_object()
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        data = json.loads(self.request.body)
        cart = Cart(self.request)
        cart.update(self.object, data.get('quantity'), 0)
        return {'msg': u'Количество товара обновлено.'}


class RemoveProduct(SingleObjectMixin, JSONResponseMixin, View):
    model = Product

    def post(self, request, *args, **kwargs):
        del kwargs['pk']
        self.object = self.get_object()
        return self.render_to_json_response(self.get_context_data(**kwargs), **kwargs)

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        cart.remove(self.object)
        return {'msg': u'Товар удален.'}
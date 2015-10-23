# -*- coding: utf-8 -*-
__author__ = 'igor'

from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic import FormView
from djangular.forms import NgModelFormMixin
from forms import Feedback
import json
from django.core.mail import send_mail
from django.http import HttpResponse
from clavutich.settings import EMAIL_COMPANY


class IndexView(TemplateView):
    template_name = 'base.html'


class FeedbackForm(NgModelFormMixin, Feedback):
    scope_prefix = 'feedback'
    form_name = 'form_comment'


class WriteToUsView(FormView, ContextMixin):
    template_name = 'write_to_us.html'
    form_class = FeedbackForm

    def post(self, request, **kwargs):
        if request.is_ajax():
            return self.ajax(request)
        return super(WriteToUsView, self).post(request, **kwargs)

    def ajax(self, request):
        form = self.form_class(data=json.loads(request.body))
        response_data = {'errors': form.errors}

        if not form.errors:
            send_mail(u'Вы получили письмо c сайта %s' % request.META['HTTP_HOST'],
                      u'Электронная почта: %s .\nКомментарий: %s' %
                      (form.cleaned_data['email'], form.cleaned_data['comment']),
                      form.cleaned_data['email'], [EMAIL_COMPANY],
                      fail_silently=False)
            response_data['msg'] = u'Ваше сообщение отправлено!'

        return HttpResponse(json.dumps(response_data), content_type="application/json")


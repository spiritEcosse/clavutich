# -*- coding: utf-8 -*-

__author__ = 'igor'

from djangular.styling.bootstrap3.forms import Bootstrap3Form
from django import forms


class Feedback(Bootstrap3Form):
    confirmation_key = forms.CharField(max_length=40, required=True, widget=forms.HiddenInput(),
                                       initial='hidden value')
    name = forms.CharField(max_length=30, label="Имя", required=False)
    email = forms.EmailField(required=True, label='Электронная почта',
                             error_messages={'required': 'Пожалуйста, введите Вашу электронную почту.'},
                             widget=forms.widgets.EmailInput(
                                 attrs={'ng-pattern': r'/^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$/'}))
    comment = forms.CharField(label='Сообщение', required=True, widget=forms.Textarea(attrs={'rows': 3}), min_length=1,
                              max_length=3000,
                              error_messages={'required': 'Пожалуйста, введите Ваше сообщение.'})

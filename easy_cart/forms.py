# -*- coding: utf-8 -*-

__author__ = 'igor'
from djangular.styling.bootstrap3.forms import Bootstrap3Form
from django import forms


class UserDataForm(Bootstrap3Form):
    confirmation_key = forms.CharField(max_length=40, required=True, widget=forms.HiddenInput(), initial='hidden value')
    name = forms.CharField(max_length=30, label="Имя", required=True,
                           error_messages={'required': 'Пожалуйста, введите Ваше имя'})
    phone = forms.RegexField(r'^\+?[0-9 .-]{4,25}$', label='Номер телефона', required=True,
                             error_messages={'invalid': 'Номер телефона должен иметь 4-25 цифр и может начинаться с +',
                                             'required': 'Пожалуйста, введите Ваш номер телефона.'},
                             widget=forms.widgets.TextInput(attrs={'ng-pattern': r'/^\+?[0-9 .-]{4,25}$/'}))
    email = forms.EmailField(required=True, help_text='На указанную электронную почту придет сообщение о заказе.',
                             label='Электронная почта',
                             error_messages={'required': 'Пожалуйста, введите Вашу электронную почту.'},
                             widget=forms.widgets.EmailInput(
                                 attrs={'ng-pattern': r'/^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$/'}))
    comment = forms.CharField(required=False, label='Сообщение', widget=forms.Textarea(attrs={'rows': 3}),
                              min_length=1, max_length=3000)


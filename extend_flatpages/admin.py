from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from extend_flatpages.models import ExtendedFlatPage
from django.forms import Textarea
from django.db import models


class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = ExtendedFlatPage
        fields = '__all__'


class ExtendedFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 40, 'rows': 4})},
    }
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'meta_title', 'meta_keywords', 'meta_description',)}),
    )


admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)
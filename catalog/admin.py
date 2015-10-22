from django.contrib import admin
from catalog.models import Category, Product
from django.contrib.admin import widgets
from catalog.widgets import ImageWidget
from django.db import models
from feincms.admin import tree_editor


class CategoryAdmin(tree_editor.TreeEditor):
    list_display = ("title", "image_preview", 'slug', 'enable', 'sort', 'date_create')
    prepopulated_fields = {'slug': ("title", )}
    formfield_overrides = {
        models.ManyToManyField: {'widget': widgets.FilteredSelectMultiple('', False, attrs={'size': '10'})},
        models.ImageField: {'widget': ImageWidget(attrs={'max_width': '100px', 'max_height': '100px'})},
    }
    list_filter = ('title', 'date_create', 'date_last_modified', 'enable')
    mptt_level_indent = 20


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", 'slug', 'enable', 'sort', 'date_create')
    prepopulated_fields = {'slug': ("title", )}
    formfield_overrides = {
        models.ManyToManyField: {'widget': widgets.FilteredSelectMultiple('', False, attrs={'size': '10'})},
        models.ImageField: {'widget': ImageWidget(attrs={'max_width': '100px', 'max_height': '100px'})},
    }
    list_filter = ('title', 'date_create', 'date_last_modified', 'enable')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
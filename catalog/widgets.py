from django import forms
from django.utils.safestring import mark_safe


class ImageWidget(forms.FileInput):
    """
    A ImageField Widget that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a class="thumbnail" href="%s">'
                           '<img src="%s" style="max-width:%s; max-height:%s;" /></a>'
                           % (value.url, value.url, self.attrs['max_width'], self.attrs['max_height'])))
        output.append(super(ImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

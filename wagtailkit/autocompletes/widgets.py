import json

from wagtailautocomplete.widgets import Autocomplete as AutocompleteBase

from .views import render_page # support uid

class Autocomplete(AutocompleteBase):
    """ Extended Autocomplete Widget, support UUID Field """

    def format_value(self, value):
        if not value:
            return 'null'
        target_model = getattr(self, 'target_model')
        if type(value) == list:
            return json.dumps([render_page(page) for page in target_model.objects.filter(pk__in=value)])
        else:
            return json.dumps(render_page(target_model.objects.get(pk=value)))

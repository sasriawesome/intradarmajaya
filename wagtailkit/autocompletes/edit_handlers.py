from wagtailautocomplete.edit_handlers import AutocompletePanel as AutocompletePanelBase, _can_create
from .widgets import Autocomplete

class AutocompletePanel(AutocompletePanelBase):

    def on_model_bound(self):
        """ This override replaces the widget with your custom version"""
        can_create = _can_create(self.target_model)
        self.widget = type(
            '_Autocomplete',
            (Autocomplete,),
            dict(target_model=self.target_model, can_create=can_create, is_single=self.is_single),
        )
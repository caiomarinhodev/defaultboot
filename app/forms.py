from django import forms
from django.forms import ModelForm
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML
from base_django.utils import generate_bootstrap_widgets_for_all_fields

from . import (
    models
)

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'


class CategoryForm(BaseForm, ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Category)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'
class Profile(BaseForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Profile)

class Category(BaseForm):
    class Meta:
        model = models.Category
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Category)

class Produto(BaseForm):
    class Meta:
        model = models.Produto
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Produto)

class Profile(BaseForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Profile)

class Category(BaseForm):
    class Meta:
        model = models.Category
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Category)

class Produto(BaseForm):
    class Meta:
        model = models.Produto
        fields = '__all__'
        widgets = generate_bootstrap_widgets_for_all_fields(models.Produto)


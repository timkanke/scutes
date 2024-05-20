from django.forms import ModelForm, RadioSelect, Select, TextInput, Textarea
from crispy_forms.helper import FormHelper
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Batch, Item


class BatchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Batch
        exclude = ['id', 'name', 'notes', 'datetime_added', 'last_export', 'export_zip']

        widgets = {'assigned_to': Select(attrs={'style': 'height:40px'})}


class ItemUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # fields that are null=true
        self.fields['date'].required = False
        self.fields['notes'].required = False
        self.fields['body_redact'].required = False
        # fields that do not save
        self.fields['date'].disabled = True
        self.fields['body_original'].disabled = True

    class Meta:
        model = Item
        fields = (
            'date',
            'reporter',
            'title',
            'body_original',
            'body_redact',
            'pool_report',
            'publish',
            'off_the_record',
            'review_status',
            'notes',
        )

        widgets = {
            'date': TextInput(attrs={'disabled': True}),
            'reporter': TextInput(attrs={'class': 'form-control'}),
            'review_status': RadioSelect(attrs={'id': 'value'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'body_redact': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends'),
            'body_original': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends'),
        }

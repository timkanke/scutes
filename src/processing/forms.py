from django.forms import ModelForm, TextInput, Textarea
from crispy_forms.helper import FormHelper
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Item


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
        fields = ('date',
                  'reporter',
                  'title',
                  'body_original',
                  'body_redact',
                  'pool_report',
                  'publish',
                  'off_the_record',
                  'review_status',
                  'notes'
                  )

        widgets = {
            'date': TextInput(attrs={'disabled': True}),
            'reporter': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'body_redact': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            ),
            'body_original': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            )
        }

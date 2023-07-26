from django.forms import ModelForm, TextInput, Textarea
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Item


class ItemUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields that are null=true
        self.fields['comment'].required = False
        self.fields['body_redact'].required = False

    class Meta:
        model = Item
        fields = ('reporter',
                  'title',
                  'body_redact',
                  'pool_report',
                  'publish',
                  'off_the_record',
                  'review_status',
                  'comment')

        widgets = {
            'reporter': TextInput(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={'class': 'form-control'}),
            'body_redact': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            )
        }

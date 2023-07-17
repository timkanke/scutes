from django import forms

# from static.django_ckeditor_5.widgets import CKEditor5Widget
from .models import Item


class ItemUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["comment"].required = False
        self.fields["body_redact"].required = False

    class Meta:
        model = Item
        fields = ('reporter',
                  'title',
                  'pool_report',
                  'publish',
                  'off_the_record',
                  'review_status',
                  'comment',
                  'body_redact')

        # you can use CKEditor5Widget in forms or models.
        # widgets = {
            # "body": CKEditor5Widget(
                # attrs={"class": "django_ckeditor_5"}, config_name="extends"
            # )
        # }

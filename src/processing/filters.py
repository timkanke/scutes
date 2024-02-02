from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, MultipleChoiceFilter

from .models import Item

PUBLISH_CHOICES = (
    (0, 'False'),
    (1, 'True'),
)

POOL_REPORT_CHOICES = (
    (0, 'False'),
    (1, 'True'),
)

OFF_THE_RECORD_CHOICES = (
    (0, 'False'),
    (1, 'True'),
)

STATUS_CHOICES = (
    (0, 'Not Started'),
    (1, 'In Progress'),
    (2, 'Complete'),
)


class ItemFilter(FilterSet):
    reporter = CharFilter(field_name='reporter', label='Reporter Name Contains', lookup_expr='icontains')
    publish = ChoiceFilter(field_name='publish', label='Publish', choices=PUBLISH_CHOICES)
    pool_report = ChoiceFilter(field_name='pool_report', label='Pool Report', choices=POOL_REPORT_CHOICES)
    off_the_record = ChoiceFilter(field_name='off_the_record', label='Off the Record', choices=(OFF_THE_RECORD_CHOICES))
    review_status = MultipleChoiceFilter(
        field_name='review_status',
        label='Editorial Review',
        choices=STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Item
        fields = (
            'reporter',
            'publish',
            'pool_report',
            'off_the_record',
            'review_status',
        )

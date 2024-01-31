from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, MultipleChoiceFilter

from .models import Item

PUBLISH_CHOICES = (
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
            'review_status',
        )

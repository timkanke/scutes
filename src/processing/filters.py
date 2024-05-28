from django import forms
from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    ModelChoiceFilter,
    MultipleChoiceFilter,
    OrderingFilter,
)
from django_filters.widgets import BooleanWidget
from django.utils.translation import gettext as _

from .models import Batch, Item, User

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


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (('', _('---------')), ('true', _('No')), ('false', _('Yes')))


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


class BatchFilter(FilterSet):
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(('name', 'name'),),
        # labels do not need to retain order
        field_labels={
            'name': 'Batch Name',
        },
    )
    name = CharFilter(field_name='name', label='Batch Name Contains', lookup_expr='icontains')
    assigned_to = ModelChoiceFilter(queryset=User.objects.all())
    last_export = BooleanFilter(
        'last_export', label='Has Been Converted', lookup_expr='isnull', widget=CustomBooleanWidget
    )
    start_date = DateFilter(
        field_name='last_export',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gt',
        label='Last Convert Date From',
    )
    end_date = DateFilter(
        field_name='last_export',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lt',
        label='Last Convert Date To',
    )

    class Meta:
        model = Batch
        fields = (
            'o',
            'name',
            'assigned_to',
            'last_export',
            'start_date',
            'end_date',
        )

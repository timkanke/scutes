from django_filters import FilterSet

from .models import Item


class ItemFilter(FilterSet):
    class Meta:
        model = Item
        fields = {
            'reporter': ['icontains'], 'review_status': ['exact']
            }
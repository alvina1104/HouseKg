from django_filters.rest_framework import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'region': ['exact'],
            'city': ['exact'],
            'district': ['exact'],
            'property_type': ['exact'],
            'price': ['gt','lt'],
            'area': ['gt','lt'],
            'rooms': ['exact'],
            'total_floor': ['gt','lt'],
            'condition': ['exact'],
            'documents': ['exact'],

        }
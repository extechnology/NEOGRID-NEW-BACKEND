from django.db.models import Q
from django_filters import rest_framework as filters
from .product_models import Product

class ProductFilter(filters.FilterSet):
    department = filters.CharFilter(method='filter_department')
    family = filters.CharFilter(method='filter_family')
    keywords = filters.CharFilter(method='filter_keywords')
    name = filters.CharFilter(method='filter_name')
    model_type = filters.CharFilter(lookup_expr='icontains')
    model_number = filters.CharFilter(lookup_expr='icontains')
    is_available = filters.BooleanFilter()
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    def filter_name(self, queryset, name, value):
        names = [item.strip() for item in value.split(',')]
        query = Q()
        for n in names:
            query |= Q(name__icontains=n)
        return queryset.filter(query)

    def filter_department(self, queryset, name, value):
        departments = [item.strip() for item in value.split(',')]
        query = Q()

        for department in departments:
            query |= Q(family__department__name__icontains=department)
            query |= Q(family__department__slug__icontains=department)

        return queryset.filter(query)

    def filter_family(self, queryset, name, value):
        families = [item.strip() for item in value.split(',')]
        query = Q()

        for family in families:
            query |= Q(family__name__icontains=family)

        return queryset.filter(query)

    def filter_keywords(self, queryset, name, value):
        keywords = [item.strip() for item in value.split(',')]
        query = Q()

        for keyword in keywords:
            query |= Q(name__icontains=keyword)
            query |= Q(model_type__icontains=keyword)
            query |= Q(model_number__icontains=keyword)
            query |= Q(description__icontains=keyword)

        return queryset.filter(query).distinct()

    class Meta:
        model = Product
        fields = []
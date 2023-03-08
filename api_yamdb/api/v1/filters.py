import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")
    name = django_filters.CharFilter(method="name_filter")

    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]

    def name_filter(self, queryset, name, value):
        return queryset.filter(name__contains=value)

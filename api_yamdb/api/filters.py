import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method="category_slug_filter")
    genre = django_filters.CharFilter(method="genre_slug_filter")

    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]

    def category_slug_filter(self, queryset, name, value):
        return queryset.filter(category__slug=value)

    def genre_slug_filter(self, queryset, name, value):
        return queryset.filter(genre__slug=value)

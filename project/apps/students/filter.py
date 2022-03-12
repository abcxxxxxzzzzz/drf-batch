import django_filters
from .models import Student, Classroom

class StudentFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    # classroom = django_filters.NumberFilter(method="search_classroom")

    # def search_classroom(self, queryset, name, value):
    #     return queryset.filter(classroom__pk=value)


    class Meta:
        model  = Student
        fields = ['name', 'classroom']


from rest_framework.filters import SearchFilter
from django.db import models
from functools import reduce
import operator
from rest_framework.compat import distinct


# 继承 SearchFilter， 重写搜索条件
class  StudentSearch(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.and_, queries))
        queryset = queryset.filter(reduce(operator.or_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)
        return queryset
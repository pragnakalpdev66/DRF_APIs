from django.db.models import Q
from django_filters import rest_framework as filters
from books.models import Books


class BookFilter(filters.FilterSet):

    filter = filters.CharFilter(method="filter_structured")
    filter_by = filters.CharFilter(method="filter_structured")

    search = filters.CharFilter(method="filter_search")
    search_by = filters.CharFilter(method="filter_search")

    sort = filters.CharFilter(method="filter_sort")

    class Meta:
        model = Books
        fields = []

    def filter_structured(self, queryset, name, value):

        queryset = Books.objects.all()
        request = self.request

        fields_param = request.query_params.get("filter", "")
        values_param = request.query_params.get("filter_by", "")

        print("filter fields:", fields_param)
        print("filter values:", values_param)

        if not fields_param or not values_param:
            return queryset

        fields = [f.strip() for f in fields_param.split(",")]
        groups = [g.strip() for g in values_param.split("|")]

        if len(fields) != len(groups):
            return queryset

        q = Q()

        for field, group in zip(fields, groups):
            temp_q = Q()
            values = [v.strip() for v in group.split(",")]
            column = Books.get_column_name(field)

            for v in values:
                print(f"Filtering {column} = {v}")
                temp_q |= Q(**{f"{column}__iexact": v})

            q &= temp_q

            print("temp_final: ",temp_q)
            print("q_after combine temp_q: ",q)

        return queryset.filter(q)

    def filter_search(self, queryset, name, value):

        queryset = Books.objects.all()
        request = self.request

        fields_param = request.query_params.get("search", "")
        values_param = request.query_params.get("search_by", "").strip()

        print("search fields:", fields_param)
        print("search value:", values_param)

        if not fields_param or not values_param:
            return queryset

        q = Q()
        fields = [f.strip() for f in fields_param.split(",")]

        for field in fields:
            column = Books.get_column_name(field)
            print("Searching column:", column)
            q |= Q(**{f"{column}__icontains": values_param})
            print("search q: ", q)

        return queryset.filter(q)

    def filter_sort(self, queryset, name, value):
        request = self.request

        field = request.query_params.get("sort", "")
        value = request.query_params.get("sort_by", "")

        if value == 'desc':
            sort_field = f"-{field}"
            print("(in if)sort_field: ",sort_field)
            return queryset.order_by(sort_field)
        elif value == 'asc':
            sort_field = field
            print("(else)sort_field: ",sort_field)
            return queryset.order_by(sort_field)
        else:
            print("defaulted values")
            return queryset.order_by('-created_at')


#  warehouse(select), refurnished (bool), sku len 12, img max size ,
#  API: seller, warehouse, currency
from rest_framework import filters
import django_filters
from products.models import Products
from django.db.models import Q
# from products.views import ProductsView

class ProductFilter(django_filters.FilterSet):
    # category__id = django_filters.UUIDFilter(field_name="category__id")

    # category__category_name = django_filters.CharFilter(field_name="category__category_name", lookup_expr='iexact')
    # brand_name = django_filters.CharFilter(field_name="brand_name", lookup_expr='icontains')
    # brand_name = django_filters.BaseInFilter(field_name="brand_name", lookup_expr='in')

    filter = django_filters.CharFilter(method="filter_structured")
    filter_by = django_filters.CharFilter(method="filter_structured")

    search = django_filters.CharFilter(method="filter_search")
    search_by = django_filters.CharFilter(method="filter_search")

    sort = django_filters.CharFilter(method="filter_sort")
    sort_by = django_filters.CharFilter(method="filter_sort")

    class Meta:
        model = Products
        fields = []
    
    queryset = Products.objects.all().filter(is_deleted=False)
    main_q = Q()
    def filter_structured(self, queryset, name, value):
    
        # queryset = Products.objects.all()
        # queryset = ProductsView.get_queryset()
        request = self.request

        # keys
        fields_param = request.query_params.get("filter", "")
        # values
        values_param = request.query_params.get("filter_by", "")

        if not fields_param or not values_param:
            return queryset

        # list of keys ('category_name','brand_name')
        fields = [f.strip() for f in fields_param.split(",")]
        # list of values separated by pipe ('c1,c2'|'b1,b2')
        groups = [g.strip() for g in values_param.split(",")]  

        print("fields: ", fields)
        print("groups: ", groups)

        # if filter_by value not entered 
        if len(fields) != len(groups):
            return queryset

        filter_q = Q()
        # category,'c1,c2' 
        # print("fields", fields)
        for field, group_values in zip(fields, groups):
            temp_q = Q()

            print("group_values: ", group_values)
            # list of values ('c1','c2')
            values = [v.strip() for v in group_values.split("|")]

            for v in values:
                print("field: ",field)
                print("v: ",v)
                # if field == "category_name":
                #     q |= Q(category__category_name__iexact=v)
                #     # temp_q = q
                
                # if field == "brand_name":
                #     q |= Q(brand_name__iexact=v)
                field_name = Products.get_column_name(field)
                print("field_name: ", field_name)
                print("field_at_fetch: ",field)
                temp_q |= Q(**{f"{field_name}__iexact" : v})
                print("temp1: ",temp_q)

            filter_q &= temp_q

            print("temp_final: ",temp_q)
            print("q_after combine temp_q: ",filter_q)

        return queryset.filter(filter_q)
    
    def filter_search(self, queryset, name, value):

        # queryset = Products.objects.all()
        request = self.request

        fields_param = request.query_params.get("search", "")
        values_param = request.query_params.get("search_by", "").strip()
        print("values_param: ", values_param)

        if not fields_param or not values_param:
            return queryset
        
        search_q = Q()

        fields = [f.strip() for f in fields_param.split(",")]
        for field in fields:
            
            print("field: ",field)
            field_name = Products.get_column_name(field)
            print('field_name: ',field_name)
            search_q |= Q(**{f"{field_name}__icontains" : values_param})

        print("q:" ,search_q)

        return queryset.filter(search_q)
    
    # sort=category,price&sort_by=asc,desc
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



   
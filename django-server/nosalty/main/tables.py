import django_tables2 as tables
from data_api.models import DataAggregator

class AdsDataTable(tables.Table):
    vacancy_name = tables.Column(attrs={'td': {'class': 'text-center'}}, verbose_name='Position')
    company_name = tables.Column(verbose_name='Company Name')
    salary_uop_min = tables.Column(verbose_name='UoP min')
    salary_uop_max = tables.Column(verbose_name='UoP max')
    salary_b2b_min = tables.Column(verbose_name='B2B min')
    salary_b2b_max = tables.Column(verbose_name='B2B max')
    url_to_offer = tables.TemplateColumn('<a href="{{record.url_to_offer}}">GO TO</a>')


    class Meta:
        model = DataAggregator
        attrs = {'class': 'table table-bordered'}
        fields = [
            'vacancy_name',
            'company_name',
            'salary_uop_min',
            'salary_uop_max',
            'salary_b2b_min',
            'salary_b2b_max'
        ]
        template_name = 'django_tables2/bootstrap4.html'

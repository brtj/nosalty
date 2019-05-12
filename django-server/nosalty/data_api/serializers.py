from rest_framework import serializers
from .models import DataAggregator

class DataAggregatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataAggregator
        fields = ('id', 'timestamp','vacancy_name', 'company_name', 'city', 'category', 'salary_uop_min', 'salary_uop_max',
                  'salary_b2b_min', 'salary_b2b_max', 'url_to_offer')
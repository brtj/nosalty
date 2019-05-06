from rest_framework import serializers
from .models import Nofluff_data

class Nofluff_dataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nofluff_data
        fields = ('id', 'timestamp','vacancy_name', 'company_name', 'city', 'category', 'salary_uop_min', 'salary_uop_max',
                  'salary_b2b_min', 'salary_b2b_max')
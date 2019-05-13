from django import forms
from data_api.models import DataAggregator


class GetReportForm(forms.Form):
    city_choice = forms.ChoiceField(choices=[], required=True)
    category_choice = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(GetReportForm, self).__init__(*args, **kwargs)
        self.fields['city_choice'].choices = DataAggregator.objects.all().values_list('city','city').distinct()
        self.fields['category_choice'].choices = DataAggregator.objects.values_list('category', 'category').distinct()

class GetCityReportForm(forms.Form):
    city_choice = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(GetCityReportForm, self).__init__(*args, **kwargs)
        self.fields['city_choice'].choices = DataAggregator.objects.all().values_list('city','city').distinct()
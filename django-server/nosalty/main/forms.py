from django import forms
from nofluff.models import Nofluff_data


class GetReportForm(forms.Form):
    city_choice = forms.ChoiceField(choices=[], required=True)
    category_choice = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(GetReportForm, self).__init__(*args, **kwargs)
        self.fields['city_choice'].choices = Nofluff_data.objects.all().values_list('city','city').distinct()
        self.fields['category_choice'].choices = Nofluff_data.objects.values_list('category', 'category').distinct()
from django.shortcuts import render, get_object_or_404, redirect
from data_api.models import DataAggregator
from main.tables import AdsDataTable
from django_tables2 import RequestConfig
import datetime
from django.db.models import Avg, Max, Min, Sum, Count, Func
from statistics import mean, median
from main.forms import GetReportForm, GetCityReportForm


def index(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    ads_today = DataAggregator.objects.filter(timestamp__range=(today_min, today_max))
    agg_cities = ads_today.values_list('city', flat=True).distinct()
    agg_categories = ads_today.values_list('category', flat=True).distinct()
    best_b2b = ads_today.order_by('-salary_b2b_max').values('vacancy_name', 'company_name', 'city',
                                                                'salary_b2b_min', 'salary_b2b_max')
    best_uop = ads_today.order_by('-salary_uop_max').values('vacancy_name', 'company_name', 'city',
                                                                'salary_uop_min', 'salary_uop_max')
    context = {
        'ALL_ads_today_count': ads_today.count(),
        'agg_cities': agg_cities,
        'agg_categories': agg_categories,
        'best_b2b': best_b2b[0],
        'best_uop': best_uop[0]
    }
    return render(request, 'main/index.html', context)


def category_report_choice(request):
    if request.method == 'POST':
        form = GetReportForm(request.POST)
        if form.is_valid():
            city_choice = form.cleaned_data['city_choice'].lower()
            category_choice = form.cleaned_data['category_choice'].lower()
            return redirect('main:category_report', city=city_choice, category=category_choice)
    else:
        form = GetReportForm()
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        ads_today = DataAggregator.objects.filter(timestamp__range=(today_min, today_max))
        agg_cities = ads_today.values_list('city', flat=True).distinct()
        agg_categories = ads_today.values_list('category', flat=True).distinct()
    context = {
        'form': form,
        'ALL_ads_today_count': ads_today.count(),
        'agg_cities': agg_cities,
        'agg_categories': agg_categories
    }
    return render(request, 'main/category_report.html', context)


def category_report(request, city, category):
    city = city.capitalize()
    category = category.capitalize()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    ads_today = DataAggregator.objects.filter(city=city, category=category, timestamp__range=(today_min, today_max))
    if ads_today:
        ads_today_table = AdsDataTable(DataAggregator.objects.filter(city=city, category=category, timestamp__range=(today_min, today_max)))
        RequestConfig(request).configure(ads_today_table)
        ads_today_uop = DataAggregator.objects.filter(city=city, category=category, timestamp__range=(today_min, today_max)).exclude(salary_uop_min__isnull=True)
        ads_today_b2b = DataAggregator.objects.filter(city=city, category=category, timestamp__range=(today_min, today_max)).exclude(salary_b2b_min__isnull=True)
        today_uop_avg = get_salary_uop_avg(ads_today_uop)
        today_uop_median = get_salary_uop_median(ads_today_uop)
        today_b2b_avg = get_salary_b2b_avg(ads_today_b2b)
        today_b2b_median = get_salary_b2b_median(ads_today_b2b)
        context = {
            'timestamp': ads_today[0].timestamp,
            'city': city.capitalize(),
            'category': category.capitalize(),
            'ads_today': ads_today,
            'ads_today_uop': ads_today_uop.count(),
            'uop_min': ads_today_uop.aggregate(Min('salary_uop_min')),
            'uop_max': ads_today_uop.aggregate(Max('salary_uop_max')),
            'uop_avg': today_uop_avg,
            'uop_med': today_uop_median,
            'ads_today_b2b': ads_today_b2b.count(),
            'b2b_min': ads_today_b2b.aggregate(Min('salary_b2b_min')),
            'b2b_max': ads_today_b2b.aggregate(Max('salary_b2b_max')),
            'b2b_avg': today_b2b_avg,
            'b2b_med': today_b2b_median,
            'ads_today_table': ads_today_table,
            }
        return render(request, 'main/category_report_output.html', context)
    else:
        context = {
            'city': city.capitalize(),
            'category': category.capitalize()
        }
        return render(request, 'main/error_report.html', context)


def get_salary_uop_avg(dict):
    avg_list = []
    if dict:
        for x in dict:
            math = (x.salary_uop_min + x.salary_uop_max) / 2
            avg_list.append(math)
        return round(mean(avg_list), 2)


def get_salary_uop_median(dict):
    med_list = []
    if dict:
        for x in dict:
            med_list.append(x.salary_uop_min)
            med_list.append(x.salary_uop_max)
        return median(med_list)


def get_salary_b2b_avg(dict):
    avg_list = []
    if dict:
        for x in dict:
            math = (x.salary_b2b_min + x.salary_b2b_max) / 2
            avg_list.append(math)
        return round(mean(avg_list), 2)


def get_salary_b2b_median(dict):
    med_list = []
    if dict:
        for x in dict:
            med_list.append(x.salary_b2b_min)
            med_list.append(x.salary_b2b_max)
        return median(med_list)


def contact(request):
    return render(request, 'main/contact.html')


def how_it_works(request):
    return render(request, 'main/how_it_works.html')


def city_report_choice(request):
    if request.method == 'POST':
        form = GetCityReportForm(request.POST)
        if form.is_valid():
            city_choice = form.cleaned_data['city_choice'].lower()
            return redirect('main:city_report', city=city_choice)
    else:
        form = GetCityReportForm()
    context = {
        'form': form,
    }
    return render(request, 'main/city_report.html', context)


class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'

def city_report(request, city):
    city = city.capitalize()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    ads_today = DataAggregator.objects.filter(city=city, timestamp__range=(today_min, today_max))
    categories_count = ads_today.values('category').annotate(total=Count('category'),
                                                             avg_uop_min=Round(Avg('salary_uop_min')),
                                                             avg_uop_max=Round(Avg('salary_uop_max')),
                                                             avg_b2b_min=Round(Avg('salary_b2b_min')),
                                                             avg_b2b_max=Round(Avg('salary_b2b_max'))
                                                             ).order_by('-total')
    print(categories_count)

    context = {
        'city': city.capitalize(),
        'ads_today': ads_today.count(),
        'categories_count': categories_count
    }
    return render(request, 'main/city_report_output.html', context)
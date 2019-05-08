from django.shortcuts import render
from nofluff.models import Nofluff_data
import datetime
from django.db.models import Avg, Max, Min, Sum
from statistics import mean, median

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def report(request, city, category):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    ads_today = Nofluff_data.objects.filter(city=city, category=category,
                                            timestamp__range=(today_min, today_max)).order_by('-timestamp')
    print(ads_today)
    if ads_today:
        ads_today_uop = Nofluff_data.objects.filter(city=city, category=category, timestamp__range=(today_min, today_max)).exclude(salary_uop_min__isnull=True)
        ads_today_b2b = Nofluff_data.objects.filter(city=city, category=category, timestamp__range=(today_min, today_max)).exclude(salary_b2b_min__isnull=True)
        today_uop_avg = get_salary_uop_avg(ads_today_uop)
        today_uop_median = get_salary_uop_median(ads_today_uop)
        today_b2b_avg = get_salary_b2b_avg(ads_today_b2b)
        today_b2b_median = get_salary_b2b_median(ads_today_b2b)
        context = {
            'city': city.capitalize(),
            'category': category.capitalize(),
            'ads_today': ads_today.count(),
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
            }
        return render(request, 'main/report.html', context)
    else:
        return render(request, 'main/error_report.html')


def get_salary_uop_avg(dict):
    avg_list = []
    if dict:
        for x in dict:
            math = (x.salary_uop_min + x.salary_uop_max) / 2
            avg_list.append(math)
        print(avg_list)
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
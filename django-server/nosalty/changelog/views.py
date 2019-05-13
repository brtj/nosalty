from django.shortcuts import render, get_object_or_404, redirect
from changelog.models import ChangeLog


def change_log(request):
    changelog = ChangeLog.objects.all().order_by('-published_at')
    context = {
        'changelog': changelog
    }
    return render(request, 'main/change_log.html', context)
from django.http import HttpResponse
from django.shortcuts import render

def map_confirmation(request):
    params = {
        'title': 'マップ確認'
    }

    return render(request, 'webtestapp/map.html', params)
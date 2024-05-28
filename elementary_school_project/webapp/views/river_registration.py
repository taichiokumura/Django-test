from django.http import HttpResponse
from django.shortcuts import render

def river_view(request):
    params = {
        'title': '川の位置を登録する'
    }

    return render(request, 'webtestapp/river.html', params)
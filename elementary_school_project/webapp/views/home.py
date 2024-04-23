from django.http import HttpResponse
from django.shortcuts import render

def home_header(request):
    params = {
        'title': '鳥獣戯画アプリ'
    }

    return render(request, 'webtestapp/home.html', params)
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch

def home_header(request):
    try:
        upstream_url = reverse('webtestapp:display_position', args=['upstream'])
        midstream_url = reverse('webtestapp:display_position', args=['midstream'])
        downstream_url = reverse('webtestapp:display_position', args=['downstream'])
    except NoReverseMatch as e:
        return HttpResponse(f"URL reverse error: {e}", status=500)
    
    params = {
        'title': '鳥獣戯画アプリ',
        'upstream_url': upstream_url,
        'midstream_url': midstream_url,
        'downstream_url': downstream_url,
    }

    return render(request, 'webtestapp/home.html', params)
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webapp.models import ImagePosition

def home_header(request):
    try:
        # year = request.session.get('year', 2024)  # デフォルト値を2024に設定
        # データベースからユニークな年度を取得し、ソートする
        years = ImagePosition.objects.values_list('year', flat=True).distinct().order_by('year')
        
        # 各川の位置に対して年度ごとのリンクを生成
        position_links = {
            year: {
                'upstream': reverse('webtestapp:display_position', args=['upstream', year]),
                'midstream': reverse('webtestapp:display_position', args=['midstream', year]),
                'downstream': reverse('webtestapp:display_position', args=['downstream', year])
            } for year in years
        }
        
    except NoReverseMatch as e:
        return HttpResponse(f"URL reverse error: {e}", status=500)
    
    params = {
        'title': '鳥獣戯画アプリ',
        'position_links': position_links,
    }

    return render(request, 'webtestapp/home.html', params)

def start_tutorial(request):
    request.session['show_tutorial'] = True
    request.session['skip_tutorial'] = False
    return JsonResponse({'status': 'started'})

def skip_tutorial(request):
    request.session['show_tutorial'] = False
    request.session['skip_tutorial'] = True
    return JsonResponse({'status': 'skipped'})


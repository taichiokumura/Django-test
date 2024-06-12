from django.http import HttpResponse
from django.shortcuts import render
import os
from django.conf import settings

def river_view(request):
    params = {
        'title': 'スライドして川の場所を選んでね'
    }

    return render(request, 'webtestapp/river.html', params)

def map_view(request, location):
    title = ''

    if location == 'upstream':
        title = '上流マップ'
    elif location == 'midstream':
        title = '中流マップ'
    elif location == 'downstream':
        title = '下流マップ'

    #セッションから画像パスを取得
    image_url = request.session.get('corrected_image_path', '')

    #デバッグ用にセッションデータをコンソールに出力
    print(f"Debug: session 'corrected_image_path': {image_url}")

    if image_url:
        relative_image_path = os.path.relpath(image_url, settings.MEDIA_ROOT).replace('\\', '/')
        image_url = os.path.join(settings.MEDIA_URL, relative_image_path)
        print(f"Debug: Full image URL: {image_url}")
    
    params = {
        'title': title,
        'image_url': image_url
    }
    
    return render(request, 'webtestapp/map.html', params)
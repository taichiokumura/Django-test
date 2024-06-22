from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from webapp.models import ImagePosition
from webapp.models import StudentInformation
import json
import os

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

    #データベースから最新の位置情報を取得
    position = ImagePosition.objects.latest('id')

    #セッションから画像パスを取得
    image_url = request.session.get('corrected_image_path', '')
    image_x = request.session.get('image_x', 0)
    image_y = request.session.get('image_y', 0)

    #デバッグ用にセッションデータをコンソールに出力
    print(f"Debug: session 'corrected_image_path': {image_url}")

    if image_url:
        relative_image_path = os.path.relpath(image_url, settings.MEDIA_ROOT).replace('\\', '/')
        image_url = os.path.join(settings.MEDIA_URL, relative_image_path)
        print(f"Debug: Full image URL: {image_url}")
    else:
        image_url = ''
    
    params = {
        'title': title,
        'image_url': image_url,
        'image_x': image_x,
        'image_y': image_y,
    }
    
    return render(request, 'webtestapp/map.html', params)

def save_position(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)

            x = data.get('x', 0)
            y = data.get('y', 0)

            #データをセッションに保存
            request.session['image_x'] = x
            request.session['image_y'] = y

            image_url = request.session.get('corrected_image_path', '')
            student_id = request.session.get('student_id', '') #学生IDをセッションから取得

            if not image_url:
                raise ValueError("Image URL is missing in the session")
            
            if not student_id:
                raise ValueError("Student ID is missing the session")
            
            #学生情報をデータベースから取得
            student = StudentInformation.objects.get_or_create(student_id=student_id)[0]

            #データベースに保存
            ImagePosition.objects.create(student=student, image_url=image_url, x=x, y=y)

            #jsonファイルに書き込む
            json_data = {
                'image_url': image_url,
                'x': x,
                'y': y,
            }

            json_file_path = os.path.join(settings.MEDIA_ROOT, 'positions.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    return JsonResponse({'status': 'failure'}, status=400)

def display_position(request):
    try:
        # JSONファイルからデータを読み込む
        # json_file_path = os.path.join(settings.MEDIA_ROOT, 'positions.json')
        # with open(json_file_path, 'r') as json_file:
        #     data = json.load(json_file)
        
        # image_url = data.get('image_url', '')
        # x = data.get('x', 0)
        # y = data.get('y', 0)

        # 最新のデータを取得
        positions = ImagePosition.objects.all()

        params_list = []
        for position in positions:
            if position.image_url:  # 修正
                relative_image_path = os.path.relpath(position.image_url, settings.MEDIA_ROOT).replace('\\', '/')
                image_url = os.path.join(settings.MEDIA_URL, relative_image_path)
            else:
                image_url = ''  # 修正: image_urlが存在しない場合の処理を追加

            params_list.append({
                'image_url': image_url,
                'x': position.x,
                'y': position.y,
            })

        print(f"Debug: x={position.x}, y={position.y}, image_url={image_url}")

        return render(request, 'webtestapp/display_position.html', {'positions': params_list})
    except Exception as e:
        return HttpResponse(f"Error loading position: {str(e)}", status=500)
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from webapp.models import ImagePosition
from webapp.models import StudentInformation
from webapp.models import CardInformation
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

    #セッションから画像パスを取得
    image_url = request.session.get('corrected_image_path', '')
    image_x = request.session.get('image_x', 0)
    image_y = request.session.get('image_y', 0)
    card_info_unique_id = request.session.get('unique_id', '') # CardInformationのunique_idをセッションから取得

    #デバッグ用にセッションデータをコンソールに出力
    print(f"Debug: session 'corrected_image_path': {image_url}")
    print(f"Debug: session 'card_info_unique_id': {card_info_unique_id}")

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
            card_info_unique_id = request.session.get('unique_id', None) # CardInformationのunique_idをセッションから取得

            if not image_url:
                raise ValueError("Image URL is missing in the session")
            
            if not student_id:
                raise ValueError("Student ID is missing the session")
            
            if not card_info_unique_id:
                raise ValueError("Card information ID is missing")
            
            #学生情報をデータベースから取得
            student = StudentInformation.objects.get_or_create(student_id=student_id)[0]

            # CardInformationを取得
            card_info = CardInformation.objects.get(unique_id=card_info_unique_id)

            # データベースに保存
            ImagePosition.objects.create(
                student=student, 
                card_info_unique_id=card_info_unique_id, 
                image_url=image_url, 
                x=x, 
                y=y
            )

            #jsonファイルに書き込む
            json_data = {
                'image_url': image_url,
                'x': x,
                'y': y,
                'unique_id': card_info_unique_id
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
        # 最新のデータを取得
        positions = ImagePosition.objects.all()

        params_list = []
        for position in positions:
            if position.image_url:  # 修正
                relative_image_path = os.path.relpath(position.image_url, settings.MEDIA_ROOT).replace('\\', '/')
                image_url = os.path.join(settings.MEDIA_URL, relative_image_path)
            else:
                image_url = ''  # 修正: image_urlが存在しない場合の処理を追加

            if position.student:
                student_id = position.student.student_id
            else:
                student_id = None

            params_list.append({
                'image_url': image_url,
                'x': position.x,
                'y': position.y,
                'student_id': student_id,
                'card_info_unique_id': position.card_info_unique_id,
            })

        print(f"Debug: x={position.x}, y={position.y}, image_url={image_url}")

        return render(request, 'webtestapp/display_position.html', {'positions': params_list})
    except Exception as e:
        return HttpResponse(f"Error loading position: {str(e)}", status=500)
    
def get_card_info(request, card_info_unique_id):
    try:
        card_infos = CardInformation.objects.filter(unique_id=card_info_unique_id)

        if not card_infos.exists():
            return JsonResponse({'status': 'failure', 'error': 'Card information not found'}, status=404)
        
        data = []
        for card_info in card_infos:
            data.append({
                'photo': card_info.photo.url,
                'observation_date_images': card_info.observation_date_images.url,
                'observation_place_images_1': card_info.observation_place_images_1.url,
                'observation_place_images_2': card_info.observation_place_images_2.url,
                'river_state_images': card_info.river_state_images.url,
                'living_thing_consideration_images': card_info.living_thing_consideration_images.url,
            })

        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from webapp.models import ImagePosition
from webapp.models import StudentInformation
from webapp.models import CardInformation
from django.urls import reverse
from django.http import HttpResponseRedirect
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

    #セッションに川の位置を保存
    request.session['location'] = location

    #セッションから画像パスを取得
    image_url = request.session.get('corrected_image_path', '')
    illustration_image = request.session.get('selected_illustration', '')
    image_x = request.session.get('image_x', 0)
    image_y = request.session.get('image_y', 0)
    card_info_unique_id = request.session.get('unique_id', '') # CardInformationのunique_idをセッションから取得

    #デバッグ用にセッションデータをコンソールに出力
    print(f"Debug: session 'corrected_image_path': {image_url}")
    print(f"Debug: session 'card_info_unique_id': {card_info_unique_id}")
    print(f"Debug: selected_illustration: {illustration_image}")

    if image_url:
        relative_image_path = os.path.relpath(image_url, settings.MEDIA_ROOT).replace('\\', '/')
        image_url = os.path.join(settings.MEDIA_URL, relative_image_path)
        print(f"Debug: Full image URL: {image_url}")
    else:
        image_url = ''
    
    params = {
        'title': title,
        'selected_illustration': illustration_image,
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
            river_location = request.session.get('location', '') # 川の位置をセッションから取得
            illustration_image = request.session.get('selected_illustration', '')

            if not image_url:
                raise ValueError("Image URL is missing in the session")
            
            if not student_id:
                raise ValueError("Student ID is missing the session")
            
            if not card_info_unique_id:
                raise ValueError("Card information ID is missing")
            
            if not river_location:
                raise ValueError("River location is missing in the session")

            #学生情報をデータベースから取得
            student = StudentInformation.objects.get_or_create(student_id=student_id)[0]

            # CardInformationを取得
            card_info = CardInformation.objects.get(unique_id=card_info_unique_id)
            year = card_info.year
            print(f"Debug: Saving position for year={year} and location={river_location}")

            # データベースに保存
            ImagePosition.objects.create(
                student=student, 
                card_info_unique_id=card_info_unique_id, 
                image_url=image_url, 
                x=x, 
                y=y,
                river_location=river_location,
                year=year,
                illustration_image=illustration_image,
            )

            #jsonファイルに書き込む
            json_data = {
                'image_url': image_url,
                'x': x,
                'y': y,
                'unique_id': card_info_unique_id,
                'location': river_location,
                'selected_illustration': illustration_image,
            }

            json_file_path = os.path.join(settings.MEDIA_ROOT, 'positions.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file)

            return JsonResponse({'status': 'success', 'location': river_location, 'card_info_unique_id': card_info_unique_id})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    return JsonResponse({'status': 'failure'}, status=400)

def save_position_and_redirect(request):
    print("Debug: Entered save_position_and_redirect function")  # 関数の最初でデバッグ
    
    response = save_position(request)
    print(f"Debug: save_position response status code: {response.status_code}")
     
    if response.status_code == 200:
        response_data = json.loads(response.content)
        print(f"Debug: Response data: {response_data}")  # レスポンスデータの内容をデバッグ
        
        if response_data['status'] == 'success':
            location = response_data['location']
            card_info_unique_id = request.session.get('unique_id')
            
            # デバッグ: セッション内の値を確認
            print(f"Debug: card_info_unique_id from session: {request.session.get('unique_id')}")
            print(f"Debug: card_info_unique_id from response: {card_info_unique_id}")
            
            if card_info_unique_id:
                card_info = CardInformation.objects.get(unique_id=card_info_unique_id)
                year = card_info.year
                print(f"Debug: Redirecting to year={year} for location={location}")
                
                # セッションの内容を確認
                print(f"Debug: Session data before redirect: {request.session.items()}")
                
                try:
                    redirect_url = reverse('webtestapp:display_position', args=[location, year])
                    print(f"Debug: redirect_url = {redirect_url}")
                except Exception as e:
                    print(f"Error: Reverse failed with location={location} and year={year}")
                    raise e
                    
                return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
            else:
                print(f"Debug: save_position failed with status code: {response.status_code}")
    return response

def display_position(request, location, year):
    try:
        # 最新のデータを取得
        # positions = ImagePosition.objects.all()
        print(f"Debug: Displaying positions for location={location}, year={year}")

        # 最新のデータを取得
        positions = ImagePosition.objects.filter(river_location=location, year=year)
        
        if not positions.exists():
            print(f"No positions found for year {year} at location {location}")

        params_list = []
        for position in positions:
            print(f"Debug: Found position with x={position.x}, y={position.y}, year={position.year}")
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
                'illustration_image': position.illustration_image,
                'image_url': image_url,
                'x': position.x,
                'y': position.y,
                'student_id': student_id,
                'card_info_unique_id': position.card_info_unique_id,
                'river_location': position.river_location,
                'year': year,
            })

        # デバッグ情報の出力はループの外に移動
        if positions:
            first_position = positions[0]
            print(f"Debug: x={first_position.x}, y={first_position.y}, image_url={first_position.image_url}")
        # print(f"Debug: x={position.x}, y={position.y}, image_url={image_url}")

        return render(request, 'webtestapp/display_position.html', {'positions': params_list, 'river_location': location, 'year': year})
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
    
    def clear_session(request):
        request.session.flush()
        return HttpResponse("Session cleared")

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime


from webapp.forms import DocumentForm
from webapp.models import CardInformation
from django.http import JsonResponse

from .login import login_qr_code
from .mark_sheet import sheet_upload
from .d_squareonly import square_cut

def index(request):
    params = {
        'title': 'カードを作る',
        'upload_form': DocumentForm(),
        'id': None,
        'login_success': None,
        'login_failure': None,
        'work_sheet_success': None,
        'work_sheet_failure': None,
    }
 
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # フォームから画像取得
                image_file = request.FILES['photo']

                # ローカル内にファイル保存
                fs = FileSystemStorage()
                filename = fs.save(image_file.name, image_file)
                uploaded_file_path = fs.path(filename)
                
                login_result = login_qr_code(request, uploaded_file_path)

                # QRコードを使ってログインを試みる
                if login_result['success'] == True:
                    card_info = form.save()
                    params['id'] = card_info.id
                    params['image_url'] = card_info.photo.url
                    
                    # ワークシート切り抜きの関数実行
                    cutout_result = square_cut(request, uploaded_file_path)

                    # 魚切り抜きの関数実行
                    # cutout_fish_result = cutout_fish(request, image_id=card_info.id)
                    
                    # マークシートの読み取り関数実行
                    # sheet_upload_result = sheet_upload(request, uploaded_file_path)
                    
                    # if cutout_fish_result['success'] == True and sheet_upload_result['success']:
                    #     params['login_success'] = 'ログインと魚の切り抜きに成功しました！'
                    #     return render(request, 'webtestapp/index.html', params)
                    # else:
                    #     fs.delete(filename)
                    #     params['login_failure'] = '魚の切り抜きに失敗しました'
                    #     if not cutout_fish_result['success']:
                    #         params['error_message'] = cutout_fish_result['error_message']
                    #     elif not sheet_upload_result['success']:
                    #         params['error_message'] = sheet_upload_result['error_message']
                    #     return render(request, 'webtestapp/index.html', params)

                    if cutout_result['success'] == True:
                        params['work_sheet_success'] = 'ワークシートの切り抜きに成功しました'
                        return render(request, 'webtestapp/index.html', params)
                    else:
                        params['work_sheet_failure'] = 'ワークシートの切り抜きに失敗しました'
                        return render(request, 'webtestapp/index.html', params)


                
                    
                else:
                    params['error_message'] = login_result['error_message']
                    fs.delete(filename)
                    params['login_failure'] = 'ログインに失敗しました'
                    return render(request, 'webtestapp/index.html', params)
            except KeyError:
                params['error_message'] = '画像がアップロードされていません'
                print(f"Debug: {params['error_message']}")
                return render(request, 'webtestapp/index.html', params)

        else:
            # フォームが無効な場合、エラーを出力
            print(form.errors)
            
    return render(request, 'webtestapp/index.html', params)
    
    

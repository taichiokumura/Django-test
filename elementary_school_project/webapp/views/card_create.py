from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime

from webapp.forms import DocumentForm
from webapp.models import CardInformation
from django.http import JsonResponse

from .login import login_qr_code #ログイン処理ファイル
from .d_squareonly import square_cut #ワークシート切り抜きファイル
from .d_sheetreader import sheet_reader #マークシート読み取りファイル
from .d_keystone import correct_keystone#台形補正ファイル

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

                #台形補正
                corrected_image_path = correct_keystone(uploaded_file_path, filename)
                
                #ログイン処理
                login_result = login_qr_code(request, corrected_image_path)

                # QRコードを使ってログインを試みる
                if login_result['success'] == True:
                    card_info = form.save()
                    params['id'] = card_info.id
                    params['image_url'] = card_info.photo.url
                    
                    # ワークシート切り抜きの関数実行
                    cutout_result = square_cut(request, corrected_image_path, card_info)

                    #マークシート読み取り関数実行
                    sheet_reader_result = sheet_reader(request, corrected_image_path)

                    if cutout_result['success'] == True and sheet_reader_result['success'] == True:
                        params['work_sheet_success'] = 'カードの作成が出来たよ'
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
    
    

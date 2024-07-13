from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
import tempfile
import os

from webapp.forms import DocumentForm
from webapp.models import CardInformation, StudentInformation
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

                temp_dir = tempfile.gettempdir()
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir=temp_dir) as temp_file:
                    for chunk in image_file.chunks():
                        temp_file.write(chunk)
                    uploaded_file_path = temp_file.name
                
                # file confirmation
                if not os.path.exists(uploaded_file_path):
                    error_message = 'Failed to create temporary file'
                    print(f"Debug: {error_message} - Path: {uploaded_file_path}")
                    params['error_message'] = error_message
                    return render(request, 'webtestapp/index.html', params)

                # ローカル内にファイル保存
                # fs = FileSystemStorage()
                # filename = fs.save(image_file.name, image_file)
                # uploaded_file_path = fs.path(filename)

                #台形補正
                corrected_image_path = correct_keystone(uploaded_file_path, os.path.basename(uploaded_file_path))
                
                #ログイン処理
                login_result = login_qr_code(request, corrected_image_path)

                # QRコードを使ってログインを試みる
                if login_result['success'] == True:
                    # 学生情報をセッションから取得
                    student_id = request.session.get('student_id')
                    student = StudentInformation.objects.get(student_id=student_id)

                    # `CardInformation` オブジェクトを作成して保存
                    card_info = form.save(commit=False)
                    card_info.student = student
                    card_info.save()
                    
                    params['id'] = card_info.id
                    params['image_url'] = card_info.photo.url
                    
                    # ワークシート切り抜きの関数実行
                    cutout_result = square_cut(request, corrected_image_path, card_info)

                    #マークシート読み取り関数実行
                    sheet_reader_result = sheet_reader(request, corrected_image_path)

                    if cutout_result['success'] == True and sheet_reader_result['success'] == True:
                        params['work_sheet_success'] = 'カードの作成が出来たよ'

                        #画像のパスをセッションに保存
                        request.session['corrected_image_path'] = corrected_image_path

                        # CardInformationのunique_idをセッションに保存
                        request.session['unique_id'] = card_info.unique_id

                        # デバッグ用にセッションデータをコンソールに出力
                        print(f"Debug: session 'corrected_image_path' set to: {corrected_image_path}")
                        print(f"Debug: session 'unique_id' set to: {request.session['unique_id']}")

                        return render(request, 'webtestapp/index.html', params)
                    else:
                        params['work_sheet_failure'] = 'ワークシートの切り抜きに失敗しました'
                        return render(request, 'webtestapp/index.html', params)
                else:
                    params['error_message'] = login_result['error_message']
                    if os.path.exists(uploaded_file_path):
                        os.remove(uploaded_file_path)
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
    
    

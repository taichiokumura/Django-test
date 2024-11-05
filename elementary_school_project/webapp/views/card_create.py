from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
from webapp.forms import DocumentForm
from webapp.models import CardInformation, StudentInformation
from .login import login_qr_code  # ログイン処理ファイル
from .d_squareonly import square_cut  # ワークシート切り抜きファイル
from .d_sheetreader import sheet_reader  # マークシート読み取りファイル
from .d_keystone import correct_keystone  # 台形補正ファイル

def index(request):
    params = {
        'title': 'カードを作る',
        'upload_form': DocumentForm(),
        'id': None,
        'login_success': None,
        'login_failure': None,
        'work_sheet_success': None,
        'work_sheet_failure': None,
        'show_tutorial': request.session.get('show_tutorial', False)  # チュートリアル表示の判定
    }

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # フォームから画像取得
                image_file = request.FILES['photo']
                selected_illustration = request.POST.get('illustration', '')
                if not selected_illustration:
                    selected_illustration = 'media/kawasemi1.png'
                print(f"Debug: Image file received: {image_file.name}")
                print(f"Debug: 選択されたイラスト： {selected_illustration}")

                # ローカル内にファイル保存
                fs = FileSystemStorage()
                filename = fs.save(image_file.name, image_file)
                uploaded_file_path = fs.path(filename)
                print(f"Debug: Image file saved at {uploaded_file_path}")
                
                # イラストをセッションに保存
                request.session['selected_illustration'] = selected_illustration

                # 台形補正
                corrected_image_path = correct_keystone(uploaded_file_path, filename)
                print(f"Debug: Keystone correction completed: {corrected_image_path}")

                # ログイン処理
                login_result = login_qr_code(request, corrected_image_path)
                print(f"Debug: Login result: {login_result}")

                # QRコードを使ってログインを試みる
                if login_result['success']:
                    print(f"Debug: Login successful for student_id: {request.session.get('student_id')}")

                    # 学生情報をセッションから取得
                    student_id = request.session.get('student_id')
                    student = StudentInformation.objects.get(student_id=student_id)

                    # `CardInformation` オブジェクトを作成して保存
                    card_info = form.save(commit=False)
                    card_info.student = student
                    card_info.year = student.year
                    card_info.save()

                    params['id'] = card_info.id
                    params['image_url'] = card_info.photo.url

                    # ワークシート切り抜きの関数実行
                    cutout_result = square_cut(request, corrected_image_path, card_info)
                    print(f"Debug: Cutout result: {cutout_result}")

                    # マークシート読み取り関数実行
                    sheet_reader_result = sheet_reader(request, corrected_image_path)
                    print(f"Debug: Sheet reader result: {sheet_reader_result}")

                    # カードの作成ができた場合の処理
                    if cutout_result['success']:
                        params['work_sheet_success'] = 'カードの作成が出来たよ'

                        # 画像のパスをセッションに保存
                        request.session['corrected_image_path'] = corrected_image_path

                        # CardInformationのunique_idをセッションに保存
                        request.session['unique_id'] = card_info.unique_id
                        
                        request.session['year'] = card_info.year

                        # デバッグ用にセッションデータをコンソールに出力
                        print(f"Debug: session 'corrected_image_path' set to: {corrected_image_path}")
                        print(f"Debug: session 'unique_id' set to: {request.session['unique_id']}")
                        print(f"Debug: session 'year' set to: {request.session['year']}")

                        # マークシート読み取りの結果を出力（失敗しても処理を進める）
                        if not sheet_reader_result['success']:
                            print(f"Warning: {sheet_reader_result['error_message']}")
                        else:
                            print(f"Success: {sheet_reader_result['success_message']}")

                        return render(request, 'webtestapp/index.html', params)

                    else:
                        params['work_sheet_failure'] = 'ワークシートの切り抜きに失敗しました'
                        print(f"Debug: Work sheet failure: Cutout success - {cutout_result['success']}")
                        return render(request, 'webtestapp/index.html', params)

                else:
                    params['error_message'] = login_result['error_message']
                    fs.delete(filename)
                    params['login_failure'] = 'ログインに失敗しました'
                    print(f"Debug: Login failed with message: {login_result['error_message']}")
                    return render(request, 'webtestapp/index.html', params)

            except KeyError as e:
                params['error_message'] = '画像がアップロードされていません'
                print(f"Debug: {params['error_message']} - {str(e)}")
                return render(request, 'webtestapp/index.html', params)

        else:
            # フォームが無効な場合、エラーを出力
            print(form.errors)

    return render(request, 'webtestapp/index.html', params)





    
    

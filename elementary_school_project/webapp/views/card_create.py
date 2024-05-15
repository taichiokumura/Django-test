from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
import os
from PIL import Image

from webapp.forms import DocumentForm
from webapp.models import CardInformation
from django.http import JsonResponse

from .login import login_qr_code
from .mark_sheet import sheet_upload

def index(request):
    params = {
        'title': 'カードを作る',
        'upload_form': DocumentForm(),
        'id': None,
        'login_success': None,
        'login_failure': None,
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
                    
                    # 魚切り抜きの関数実行
                    cutout_fish_result = cutout_fish(request, image_id=card_info.id)
                    
                    # マークシートの読み取り関数実行
                    sheet_upload_result = sheet_upload(request, uploaded_file_path)
                    
                    if cutout_fish_result['success'] == True and sheet_upload_result['success'] == True:
                        params['login_success'] = 'ログインと魚の切り抜きに成功しました！'
                        return render(request, 'webtestapp/index.html', params)
                    else:
                        fs.delete(filename)
                        params['login_failure'] = '魚の切り抜きに失敗しました'
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

from io import BytesIO

import cv2
import numpy as np
import math
import os

def cutout_fish(request, image_id=0):

    # 比率調整
    w_ratio = 1.1

    upload_image = get_object_or_404(CardInformation, id=image_id)
    print(f"Debug: upload_image - {upload_image}")

    # 画像のパスを取得
    image_path = upload_image.photo.path
    print(f"Debug: Image Path - {image_path}")

    # 出力ディレクトリのパス
    # 新しいファイル名を作成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"cutout_image_{timestamp}.png"

    # OpenCVでグレースケール画像を保存,新しいファイル名で保存
    cutout_image_path = os.path.join(settings.MEDIA_ROOT, 'result_images', new_filename)
    cutout_url = os.path.join(settings.MEDIA_URL, 'result_images', new_filename)

    # models.pyからcutout_imageを呼び出す
    upload_image.cutout_image(cutout_url)

    # 指定された矩形領域内の4つの座標
    p1 = (184, 217)
    p2 = (670, 217)
    p3 = (184, 440)
    p4 = (670, 440)

    # 入力画像の読み込み
    img = cv2.imread(image_path)

    # 幅取得
    o_width = p2[0] - p1[0]
    o_width = math.floor(o_width * w_ratio)

    # 高さ取得
    o_height = p3[1] - p1[1]
    o_height = math.floor(o_height)

    # 変換前の4点
    src = np.float32([p1, p2, p3, p4])

    # 変換後の4点
    dst = np.float32([[0, 0], [o_width, 0], [0, o_height], [o_width, o_height]])

    # 変換行列
    M = cv2.getPerspectiveTransform(src, dst)

    # 射影変換・透視変換する
    output = cv2.warpPerspective(img, M, (o_width, o_height))

    # グレースケールに変換
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    # エッジ検出
    edges = cv2.Canny(gray, 200, 400)

    # 輪郭抽出
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # すべての輪郭を切り出して保存
    for i, contour in enumerate(contours):
        # 輪郭を囲む矩形を取得
        x, y, w, h = cv2.boundingRect(contour)

        # 輪郭が指定された矩形領域内にあり、かつ一番外側の輪郭の場合のみ切り出し
        if x >= 0 and y >= 0 and x + w <= o_width and y + h <= o_height:
            # 切り出し領域を取得
            cropped = output[y:y+h, x:x+w]

            # 輪郭線の外側を透過処理
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.drawContours(mask, [contour - (x, y)], 0, (255, 255, 255), -1)
            alpha = np.zeros_like(mask, dtype=np.uint8)
            alpha[mask == 255] = 255
            b, g, r = cv2.split(cropped)
            rgba = [b, g, r, alpha]
            transparent_img = cv2.merge(rgba, 4)

            # 切り出し領域の保存
            cv2.imwrite(cutout_image_path, transparent_img)
            print(f"切り抜けました")
            return {'success': True}

        else:
            print(f"切り抜けませんでした")
            return {'success': False, 'error_message': '画像が切り抜けませんでした。'}
    
    

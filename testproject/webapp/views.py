from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from .forms import DocumentForm
from .models import Document

def index(request):
    params = {
        'title': '画像のアップロード',
        'upload_form': DocumentForm(),
        'id': None,
    }
 
    if (request.method == 'POST'):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload_image = form.save()
 
            params['id'] = upload_image.id
 
    return render(request, 'webtestapp/index.html', params)



# def preview(request, image_id=0):
 
#     upload_image = get_object_or_404(Document, id=image_id)
 
#     params = {
#         'title': '画像の表示',
#         'id': upload_image.id,
#         'url': upload_image.photo.url
#     }
 
#     return render(request, 'webtestapp/preview.html', params)

from PIL import Image
from io import BytesIO

def preview(request, image_id=0):
    upload_image = get_object_or_404(Document, id=image_id)
    print(f"Debug: upload_image - {upload_image}")

    # 画像のパスを取得
    image_path = upload_image.photo.path
    print(f"Debug: Image Path - {image_path}")

    # Pillowを使用して画像を読み込む
    img = Image.open(image_path)
    
    # 画像を白黒に変換
    gray_img = img.convert('L')

    # 白黒画像を保存
    bw_image_path = os.path.join(settings.MEDIA_ROOT, 'result_images', 'bw_image.jpg')
    gray_img.save(bw_image_path)
    
    bw_url = os.path.join(settings.MEDIA_URL, 'result_images', 'bw_image.jpg')

    params = {
        'title': '画像の表示',
        'id': upload_image.id,
        'url': upload_image.photo.url,
        'bw_url': bw_url  # 白黒画像のURLを追加
    }

    return render(request, 'webtestapp/preview.html', params)
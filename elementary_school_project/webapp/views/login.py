import json
import cv2
from django.http import JsonResponse
from pyzbar.pyzbar import decode
from webapp.models import StudentInformation

def login_qr_code(request, upload_image):
    # 画像からQRコードを読み取る
    decode_objects = decode(cv2.imread(upload_image.photo.path))

    if decode_objects:
        # QRコードから読み取った学籍番号
        decode_student_id = decode_objects[0].data.decode('utf-8')

        try:
            # データベースから学籍番号を取得
            student = StudentInformation.objects.get(student_id=decode_student_id)

            # ログインに成功した場合はセッションに保存
            request.session['student_id'] = decode_student_id
            print(f"ログインに成功しました。学籍番号: {decode_student_id}")

            # ログイン成功をJSON形式で返す
            return JsonResponse({'success': True, 'student_id': decode_student_id})
        except StudentInformation.DoesNotExist:
            # ログイン失敗をJSON形式で返す
            return print(f"ログインに失敗しました。")
    else:
        # QRコードが見つからなかった場合はログイン失敗とみなす
        return print(f"QRコードが見つかりませんでした。")




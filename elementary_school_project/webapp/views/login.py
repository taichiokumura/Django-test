# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from webapp.models import StudentInformation
# import cv2
# from pyzbar.pyzbar import decode

# def login_card(request):
#     if request.method == 'POST':
#         # 画像ファイルを受け取る
#         upload_image = request.FILES['image']

#         # 画像からQRコードを読み取る
#         decode_objects = decode(cv2.imread(upload_image))

#         if decode_objects:
#             # QRコードから読み取った学籍番号
#             decode_student_id = decode_objects[0].data.decode('utf-8')

#             try:
#                 # データベースから学籍番号を取得
#                 student = StudentInformation.objects.get(student_id=decode_student_id)

#                 # ログインに成功した場合はセッションに保存
#                 request.session['student_id'] = decode_student_id
#                 print(f"ログインに成功しました。学籍番号: {decode_student_id}")

#                 return render(request, 'webtestapp/index.html', {'error_message': error_message})
#             except StudentInformation.DoesNotExist:
#                 error_message = '学籍番号が正しくありません'
#                 print(error_message)  # ターミナルにエラーメッセージを表示
#         else:
#             error_message = 'QRコードが見つかりませんでした'
#             print(error_message)  # ターミナルにエラーメッセージを表示
#     else:
#         error_message = None

#     return render(request, 'webtestapp/index.html', {'error_message': error_message})




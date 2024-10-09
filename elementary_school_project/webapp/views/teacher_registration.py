from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import openpyxl.workbook
from webapp.forms import StudentInformationForm
from webapp.models import StudentInformation
import openpyxl
from django.conf import settings
import os

def account_registration(request):
    if request.method == 'POST':
        form = StudentInformationForm(request.POST)
        if form.is_valid():
            # フォームデータを保存
            student = form.save()

            # Excelファイルへのパスを設定
            excel_path = os.path.join(settings.MEDIA_ROOT, 'students.xlsx')

            try:
                # MEDIA_ROOTフォルダが存在しない場合、作成
                if not os.path.exists(settings.MEDIA_ROOT):
                    print(f"MEDIA_ROOTが存在しないため作成します: {settings.MEDIA_ROOT}")
                    os.makedirs(settings.MEDIA_ROOT)

                # Excelファイルが存在する場合は開き、存在しない場合は新規作成
                if os.path.exists(excel_path):
                    print(f"既存のExcelファイルにデータを追加します: {excel_path}")
                    wb = openpyxl.load_workbook(excel_path)
                    ws = wb.active
                else:
                    print(f"Excelファイルが存在しないため作成します: {excel_path}")
                    wb = openpyxl.Workbook()
                    ws = wb.active
                    ws.title = "Students"

                    # ヘッダー行を追加
                    ws.append(['名前', '名前ID', '学生ID', '年度'])
                
                # 新しいデータを追加
                ws.append(['', student.name_id, student.student_id, student.year])
                wb.save(excel_path)
                print(f"Excelファイルにデータを追加しました: {excel_path}")

            except Exception as e:
                print(f"エラーが発生しました: {str(e)}")
                return JsonResponse({'success': False, 'error': str(e)})

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # GETリクエストの場合
    else:
        form = StudentInformationForm()
        students = StudentInformation.objects.all()
        return render(request, 'webtestapp/teacher_registration.html', {'form': form, 'students': students})


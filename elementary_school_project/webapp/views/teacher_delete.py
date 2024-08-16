from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from webapp.models import StudentInformation
from webapp.forms import StudentInformationForm

# 学生情報削除関数
def delete_student(request, student_id):
    student = get_object_or_404(StudentInformation, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
# teacher_registration.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from webapp.forms import StudentInformationForm
from webapp.models import StudentInformation

# 関数名を修正
def account_registration(request):
    if request.method == 'POST':
        form = StudentInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = StudentInformationForm()

    students = StudentInformation.objects.all()

    return render(request, 'webtestapp/teacher_registration.html', {'form': form, 'students': students})

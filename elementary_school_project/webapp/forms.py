from django import forms
from .models import CardInformation
from .models import StudentInformation
from django.core.exceptions import ValidationError
import re

class DocumentForm(forms.ModelForm):

    class Meta:
        model = CardInformation
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'capture': 'environment'})
        }

class AquaticLifeDiscoveryForm(forms.Form):
    name = forms.CharField(label='水生生物の名前', max_length=100)

class StudentInformationForm(forms.ModelForm):
    class Meta:
        model = StudentInformation
        fields = ['student_name','student_id','year'] #フォームで入力するフィールド
        widgets = {
            'student_name': forms.TextInput(attrs={'placeholder': '名前を入力'}),
            'student_id': forms.TextInput(attrs={'placeholder': '学籍番号を入力'}),
            'year': forms.NumberInput(attrs={'value': 2024}),
        }
        labels = {
            'student_name': '名前',
            'student_id': 'パスワード',
            'year': '年度'
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')

        #パスワードが英文字と数字のみで構成されているか確認
        if not re.match(r'^[a-zA-Z0-9]+$', student_id):
            raise ValidationError('学籍番号は英文字と数字のみ使用できます。')
        return student_id
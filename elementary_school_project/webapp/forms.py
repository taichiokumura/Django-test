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
        fields = ['name_id','student_id','year'] #フォームで入力するフィールド
        widgets = {
            'name_id': forms.TextInput(attrs={'placeholder': 'IDを入力'}),
            'student_id': forms.TextInput(attrs={'placeholder': '学籍番号を入力'}),
            'year': forms.NumberInput(attrs={'value': 2024}),
        }
        labels = {
            'name_id': '名前ID',
            'student_id': 'パスワード',
            'year': '年度'
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')

        #パスワードが英文字と数字のみで構成されているか確認
        if not re.match(r'^[a-zA-Z0-9]+$', student_id):
            raise ValidationError('学籍番号は英文字と数字のみ使用できます。')
        return student_id
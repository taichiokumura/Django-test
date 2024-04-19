from django import forms
from .models import CardInformation

class DocumentForm(forms.ModelForm):

    # 魚の種類を選ぶラジオボタン
    fish_choices = [
        ('1', 'メダカ'),
        ('2', 'キンブナ'),
        ('3', 'シマドジョウ'),
        ('4', 'タイリクバラタナゴ'),
    ]

    fish = forms.ChoiceField(
        choices=fish_choices,
        widget=forms.RadioSelect,
    )

    # 説明用のテキストエリア
    explanation = forms.CharField(
        widget=forms.Textarea,
        label='説明'
    )

    class Meta:
        model = CardInformation
        fields = ['photo', 'fish', 'explanation']
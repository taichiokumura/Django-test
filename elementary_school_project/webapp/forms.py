from django import forms
from .models import CardInformation

class DocumentForm(forms.ModelForm):

    class Meta:
        model = CardInformation
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'capture': 'environment'})
        }

class AquaticLifeDiscoveryForm(forms.Form):
    name = forms.CharField(label='水生生物の名前', max_length=100)
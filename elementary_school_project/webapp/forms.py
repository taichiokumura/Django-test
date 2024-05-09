from django import forms
from .models import CardInformation

class DocumentForm(forms.ModelForm):

    class Meta:
        model = CardInformation
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'capture': 'environment'})
        }
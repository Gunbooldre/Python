from django import forms

from cities.models import City

class HTMLForm(forms.Form):
    name = forms.CharField(label='Город')

class cityForm(forms.ModelForm):
    name = forms.CharField(label = 'Город', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите название города'}))
        
    class Meta:
        model = City
        fields = ('name',)
from django import forms

from plains.models import Plain
from cities.models import City



class PlainForm(forms.ModelForm):
    name = forms.CharField(label = 'Номер Самолета', widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите  Номер Самолета'}))
    travel_time = forms.IntegerField(label = 'Время в пути',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Время в пути'}))
    fromCity = forms.ModelChoiceField(label = 'Откуда', queryset = City.objects.all(),widget = forms.Select(attrs={
            'class': 'form-control',}))
    toCity = forms.ModelChoiceField(label = 'Куда', queryset = City.objects.all(),widget=forms.Select(attrs={
            'class': 'form-control',}))
    class Meta:
        model = Plain
        fields = '__all__'
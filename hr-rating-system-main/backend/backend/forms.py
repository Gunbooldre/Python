from django import forms
from .models import ListPeopleModel, UsersModel

responsiveness = (
    ("-", "-"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)
friendliness = (
    ("-", "-"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)
class UserEvaluationForm(forms.ModelForm):
    name = forms.CharField(label="Имя",disabled=True)
    dep = forms.CharField(label="Депортамент",disabled=True)
    responsiveness = forms.ChoiceField(choices=responsiveness,label = "Ответсвенность",widget = forms.Select(attrs={
        'class': 'form-control',}))
    friendliness = forms.ChoiceField(choices =friendliness ,label="Дружелюбие", widget=forms.Select(attrs={
        'class': 'form-control', }))

    def clean(self):
        clean_data = super(UserEvaluationForm, self).clean()
        responsiveness = clean_data.get('responsiveness')
        friendliness = clean_data.get('friendliness')
        if  (responsiveness or friendliness) == '-':
            raise forms.ValidationError('Укажите свою оценку пожалуйста')

    class Meta:
        model = ListPeopleModel
        fields = ['name','dep','responsiveness', 'friendliness']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = UsersModel.objects.get(login=username)
        except UsersModel.DoesNotExist:
            raise forms.ValidationError("Invalid login")

        if user.password != password:
            raise forms.ValidationError("Invalid password")

        return self.cleaned_data
    

from django import forms
from .models import ListPeopleModel, UsersModel, ListBossModel
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


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
    def __init__(self, *args, **kwargs):
        super(UserEvaluationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'input_like_label form-control form-control-lg'
        self.fields['dep'].widget.attrs['class'] = 'input_like_label form-control form-control-lg'
        self.fields['responsiveness'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['friendliness'].widget.attrs['class'] = 'form-control form-control-lg'

    name = forms.CharField(label="Сотрудник", disabled=False)
    dep = forms.CharField(label="Департамент", disabled=False)
    responsiveness = forms.ChoiceField(choices=responsiveness, label="Отзывчивость", widget=forms.Select(attrs={
        'class': 'form-control', }))
    friendliness = forms.ChoiceField(choices=friendliness, label="Доброжелательность", widget=forms.Select(attrs={
        'class': 'form-control', }))

    def clean(self):
        clean_data = super(UserEvaluationForm, self).clean()
        responsiveness = clean_data.get('responsiveness')
        friendliness = clean_data.get('friendliness')
        if (responsiveness or friendliness) == '-':
            raise forms.ValidationError('Укажите свою оценку пожалуйста')

    class Meta:
        model = ListPeopleModel
        fields = ['name', 'dep', 'responsiveness', 'friendliness']


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-lg'

    username = forms.CharField(required=True, label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Введите Ваш логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введите Ваш пароль'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = UsersModel.objects.get(login=username)
        except UsersModel.DoesNotExist:
            raise forms.ValidationError("Неверный login")

        if user.password != password:
            raise forms.ValidationError("Неверный password")

        return self.cleaned_data

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForma(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForma, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control form-control-lg'

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "Your old password was entered incorrectly. Please enter it again."
        ),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password
    
    

class NewEmployedForm(forms.ModelForm):
    class Meta:
        model = ListPeopleModel
        fields = ['name', 'dep']
        widgets = {
            'dep': forms.Select(choices=[('', ''), 
                                         ('HR Team', 'HR Team'), 
                                         ('Education Team', 'Education Team'), 
                                         ('Legal Team', 'Legal Team'),
                                         ('General Affair Team', 'General Affair Team'), 
                                         ('Accounting/Financial Team', 'Accounting/Financial Team'), 
                                         ('New business', 'New business'),
                                         ('Screening Team', 'Screening Team'), 
                                         ('Collection Team', 'Collection Team'), 
                                         ('Risk Team', 'Risk Team'),
                                         ('ICT Team', 'ICT Team'), 
                                         ('Сustomer service Team', 'Сustomer service Team'), 
                                         ('Sales Planning Team', 'Sales Planning Team'),
                                         ('Sales Team 1', 'Sales Team 1'), 
                                         ('Сredit administration Team ', 'Сredit administration Team '), 
                                         ('Nur-Sultan', 'Nur-Sultan'),
                                         ('Shymkent', 'Shymkent'),    
                                         ], 
                                attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
       
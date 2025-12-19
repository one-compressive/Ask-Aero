from django import forms
from django.contrib.auth import authenticate
from django.forms.widgets import PasswordInput
from django.forms.widgets import FileInput

from app.models import Question, User, Answer

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        max_length=128,
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'current-password'
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    'Неверное имя пользователя или пароль'
                )

        return cleaned_data

class QuestionForm(forms.ModelForm):
    image = forms.ImageField(widget=FileInput, required=False)

    class Meta:
        model = Question
        fields = ('title', 'text') #'tags'

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'new-password'
        }),
    )
    password_repeat = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        }),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

class AnswerForm(forms.ModelForm):
    widgets = {
        'answer_text': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш ответ здесь...',
            'rows': 5
        })
    }
    class Meta:
        model = Answer
        fields = ('answer_text',)


from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SimplifiedUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        min_length=4,
        help_text=""
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        min_length=4,
        help_text="Введите ещё раз"
    )
    
    username = forms.CharField(
        label="Имя пользователя",
        max_length=160,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'имя пользователя'}),
        help_text=""
    )
    
    class Meta:
        model = User
        fields = ('username',)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError("не может быть пустым")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Пользователь '{username}' уж есть")
        
        return username
    
    def clean(self):
     
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("неверно")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

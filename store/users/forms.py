from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def validate_email_unique(value):
	if User.objects.filter(email=value):
		raise ValidationError("""
		Введенный вами адрес электронный почту уже зарегистрирован!
		Пожалуйста, используйте соответствующий профиль или зарегистрируйтесь с другим адресом.
		""")

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(validators=[validate_email_unique])

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
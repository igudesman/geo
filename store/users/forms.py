from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def validate_email_unique(value):
	exists = User.objects.filter(email=value)
	if exists:
		raise ValidationError("A user with that email already exists.")

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(validators=[validate_email_unique])

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
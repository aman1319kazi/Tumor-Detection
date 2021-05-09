from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

		labels={ 
			'username' : _('Username'),
			'email' : _('Email'),
			'password1' : _('Password'),
			'password2' : _('Confirm Password')
			}

widgets = {
		'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id':'inputusername'}),
		'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email','id':'inputEmail'}),
		'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password','id':'inputPassword'}),
		'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password','id':'inputPassword'}),
		}
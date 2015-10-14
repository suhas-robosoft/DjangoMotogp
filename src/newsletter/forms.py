from django import forms
from django.contrib.auth.models import User

import re

from .models import SignUp

class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField()

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_base, provider = email.split("@")
		domain, extension = provider.split(".")
		if domain != 'gmail':
			raise forms.ValidationError("please provide a gmail id")
		return email

	def clean_full_name(self):
		name = self.cleaned_data.get('full_name')

		if re.search(r"[0-9]", name):
			raise forms.ValidationError("please provide a valid name")
		elif not name:
			name = 'Anonymous'
		return name

class SignUpForm(forms.ModelForm):
	class Meta:
		model = SignUp
		fields = ['full_name', 'email']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_base, provider = email.split("@")
		domain, extension = provider.split(".")
		if domain != 'gmail':
			raise forms.ValidationError("please provide a gmail id")
		return email

	def clean_full_name(self):
		name = self.cleaned_data.get('full_name')

		if re.search(r"[0-9]", name):
			raise forms.ValidationError("please provide a valid name")
		return name

class RegistrationForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)
	password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_base, provider = email.split("@")
		domain, extension = provider.split(".")
		if domain != 'gmail':
			raise forms.ValidationError("please provide a gmail id")
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username= username).exists():
			raise forms.ValidationError("Username already taken, try a new one")
		return username

	def clean_password_confirmation(self):
		password_confirm = self.cleaned_data.get('password_confirmation')
		if self.cleaned_data.get('password') != password_confirm :
			raise forms.ValidationError("Passwords don't match")
		return password_confirm
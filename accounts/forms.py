from django.contrib.auth import authenticate, get_user_model
from django import forms
from .models import Profile

class UsersLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput,)

	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("This user does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active")

		return super(UsersLoginForm, self).clean(*args, **keyargs)

User = get_user_model()

class UsersRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"confirm_email", 
			"password",
		]
	username = forms.CharField()
	email = forms.EmailField(label = "Email")
	confirm_email = forms.EmailField(label = "Confirm Email")
	password = forms.CharField(widget = forms.PasswordInput)


	def __init__(self, *args, **kwargs):
		super(UsersRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['email'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"email"})
		self.fields['confirm_email'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"confirm_email"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})


	def clean(self, *args, **keyargs):
		email = self.cleaned_data.get("email")
		confirm_email = self.cleaned_data.get("confirm_email")
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if email != confirm_email:
			raise forms.ValidationError("Email must match")
		
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email is already registered")

		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("User with this username already registered")
		
		#you can add more validations for password

		if len(password) < 8:	
			raise forms.ValidationError("Password must be greater than 8 characters")


		return super(UsersRegisterForm, self).clean(*args, **keyargs)
 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'github_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        website_url = forms.CharField(required=False)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
		

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission,Group
from tasks.forms import StyleFormMixin
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None
            
class CustomRegistrationForm(StyleFormMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
         
        if len(password1)<8:
            errors.append('Password mush be at least 8 characters long')
        if not re.search('[A-Z]', password1):
            errors.append("Your password must contain at least one uppercase letter.")
        if not re.findall('[a-z]', password1):
            errors.append("Your password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password1):
            errors.append("Your password must contain at least one number.")
        if not re.findall("[!@#$%^&*()-_+={}[]|\\;:'\"<>,./?]", password1):
            errors.append("Your password must contain at least one special character.")
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email=email).exists()
        
        if email_exist:
            raise forms.ValidationError("Email already exists")

        return email
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match")
        
        return cleaned_data
        
class LoginForm(StyleFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class AssignRoleForm(StyleFormMixin,forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Select a Role'
    )
    class Meta:
        model = User
        fields = []
    
class CreateGroupForm(StyleFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name','permissions']
        
class CustomPasswordChangeForm(StyleFormMixin,PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyleFormMixin,PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyleFormMixin,SetPasswordForm):
    pass

"""
class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']
    
    bio = forms.CharField(required=False,widget=forms.Textarea,label='Bio')
    profile_image = forms.ImageField(required=False,label='Profile Image')
    
    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile',None)
        super().__init__(*args, **kwargs)
        
        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image
            
    def save(self, commit = True):
        user = super().save(commit=False)
        
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')
            
            if commit:
                self.userprofile.save()
        
        if commit:
            user.save()
            
        return user     
"""        

class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','bio','profile_image']
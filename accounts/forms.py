'''
write a Registration Form using Account Model with additional form fields name password and confirm_password
'''
from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone']

    '''
    write a method to apply css to the all forms fields
    '''
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Enter Confirm Password'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control'

    '''
    write a clean method to check if password and confirm_password are same or not and return validation error if password and confirm_password are not matching
    '''
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password and Confirm Password must be same')

'''
write a User Form using Account Model
'''
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone']
        # email field is defined inside html

    '''
    write a method to apply css to the all forms fields
    '''
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

'''
Write a User Profile Form using User Profile Model
'''
class UserProfileForm(forms.ModelForm):

    profile_pic = forms.ImageField(required=False, error_messages={'invalid': ('remove currently stored picture path')}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'pincode', 'state', 'country', 'profile_pic']

    '''
    write a method to apply css to the all forms fields
    '''
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
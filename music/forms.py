from django.contrib.auth.models import User 
from django import forms

class UserForm(forms.ModelForm):  #here we are creating userform
    password = forms.CharField(widget=forms.PasswordInput)  #password field

    class Meta: #this Meta class is basically information about your class
        model = User #here if new user create than it will store to the database
        fields = ['username','email','password'] #and here the fields which are display onto the form

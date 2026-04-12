from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", 'email',]


    #Function to accept only bard emails
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@bard.edu"):
            raise ValidationError("Sorry, this platform is currently restricted to Bard College students. You must use an @bard.edu email address.")
        return email
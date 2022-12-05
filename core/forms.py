from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, User
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TripForm(ModelForm):
    class Meta:
        model = Trip
        widgets = {'start_date': DateInput(),
                   'end_date': DateInput()}
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'avatar', 'bio']


class myUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

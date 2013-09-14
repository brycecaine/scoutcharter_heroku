from advancement.models import Scouter
from django import forms
from django.contrib.auth.models import User

class ScouterForm(forms.Form): 
    username = forms.CharField(max_length=30, min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))

    def save(self, commit=True):
        scouter = super(ScouterForm, self).save()

    def clean_username(self):
        if self.errors:
            return self.cleaned_data

        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError('%s already exists' % username)

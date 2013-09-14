from advancement.models import Scouter
from django import forms
from django.contrib.auth.models import User

class ScouterForm(forms.Form): 
    username = forms.CharField(max_length=30, min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ScouterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']

        if self.user.username != username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return username

            raise forms.ValidationError('%s already exists' % username)

        else:
            return username

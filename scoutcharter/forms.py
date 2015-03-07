from advancement.models import Rank, Scouter
from django import forms
from django.contrib.auth.models import User

ROLES = (('', '---------'), ('leader', 'Leader'), ('parent', 'Parent'), ('scout', 'Scout'), )
PATROLS = (('', '---------'), ('all', 'All'), ('troop', 'Troop'), ('team', 'Team'), ('crew', 'Crew'), )

class ScouterForm(forms.Form): 
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=30, min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    role = forms.ChoiceField(choices=ROLES)
    patrol = forms.ChoiceField(choices=PATROLS)
    rank = forms.ModelChoiceField(queryset=Rank.objects.all().order_by('weight'))

    def __init__(self, username, mode, *args, **kwargs):
        self.username = username
        self.mode = mode
        super(ScouterForm, self).__init__(*args, **kwargs)

    def check_existing(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError('%s already exists' % username)

    def clean_username(self):
        username = self.cleaned_data['username']

        if (self.mode == 'E' and self.username != username) or self.mode == 'A':
            return self.check_existing(username)
        else:
            return username
            

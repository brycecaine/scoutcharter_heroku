from advancement.models import Scouter
from django.forms import ModelForm

class ScouterForm(ModelForm): 
    class Meta:
        model = Scouter
        fields = ('birth_date','phone_number')

    def save(self, commit=True):
        scouter = super(ScouterForm, self).save()

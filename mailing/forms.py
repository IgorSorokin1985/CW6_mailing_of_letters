from django import forms
from mailing.models import Mailing


class MailingForm(forms.ModelForm):
    """
    This form for creating and updating mailing.
    """

    class Meta:
        model = Mailing
        exclude = ('user', 'status',)
        #widgets = {'data_mailing': forms.DateTimeInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

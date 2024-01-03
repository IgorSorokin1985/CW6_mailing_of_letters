from django import forms
from mailing.models import Mailing


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('user', 'status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

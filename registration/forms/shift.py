from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ..models import Shift


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        exclude = ['job', ]
        widgets = {
            'begin': forms.DateTimeInput(attrs={'class': 'datetime'}),
            'end': forms.DateTimeInput(attrs={'class': 'datetime'}),
        }

    def __init__(self, *args, **kwargs):
        self.job = kwargs.pop('job')

        super(ShiftForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(ShiftForm, self).clean()

        if self.cleaned_data['begin'] > self.cleaned_data['end']:
            raise ValidationError(_("The begin of the shift must be before "
                                    "the end."))

    def save(self, commit=True):
        instance = super(ShiftForm, self).save(False)  # event is missing

        # add event
        instance.job = self.job

        if commit:
            instance.save()

        return instance


class ShiftDeleteForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = []

    def delete(self):
        self.instance.delete()
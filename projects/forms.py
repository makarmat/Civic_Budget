from datetime import datetime
from dateutil.relativedelta import relativedelta
from .widgets import BootstrapDateTimePickerInput
from .widgets import FengyuanChenDatePickerInput
from bootstrap_daterangepicker import fields, widgets
from django import forms
from .models import VERIFIED, Voter
from django.core.exceptions import ValidationError

from projects.models import Originator, Project, Cost


def validate_pesel(pesel):
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    p_list = [int(d) for d in pesel]
    l_ratio = [weights[i]*p_list[i] for i in range(len(weights))]
    result = 10 - (sum(l_ratio) % 10)
    majority_date = datetime.now() - relativedelta(years=18)
    if result != p_list[-1]:
        raise ValidationError('Numer PESEL jest nieprawidłowy!')
    elif int(pesel[2:4]) > 20:
        birth_date = datetime(int("20" + pesel[0:2]), int(pesel[2:4]) - 20, int(pesel[4:6]))
        if birth_date >= majority_date:
            raise ValidationError('Osoba nie ma ukończonych 18 lat!')
    else:
        birth_date = datetime(int("19" + pesel[0:2]), int(pesel[2:4]), int(pesel[4:6]))
        if birth_date >= majority_date:
            raise ValidationError('Osoba nie ma ukończonych 18 lat!')


def validate_phone(value):
    phone_number = str(value)
    if len(phone_number) != 9:
        raise ValidationError('Numer telefonu powinien mieć formę: "510123456"!')


class AddOriginatorForm(forms.ModelForm):
    pesel = forms.CharField(validators=[validate_pesel], widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    phone = forms.IntegerField(label='Numer telefonu', validators=[validate_phone])

    class Meta:
        model = Originator
        fields = '__all__'


MONTHS = {
    7: 'lipiec', 8: 'sierpień', 9: 'wrzesień',
    10: 'październik', 11: 'listopad', 12: 'grudzień'
}


class AddProjectDetailForm(forms.ModelForm):
    originator_id = forms.IntegerField(widget=forms.HiddenInput())
    # start_date = forms.DateField(widget=forms.SelectDateWidget(months=MONTHS, years=[2019]), label='Data rozpoczęcia:')
    # end_date = forms.DateField(widget=forms.SelectDateWidget(months=MONTHS, years=[2019]), label='Data zakończenia:')
    start_date = forms.DateField(input_formats=['%Y-%m-%d'],
                                 label='Data rozpoczęcia:',
                                 widget=FengyuanChenDatePickerInput(
                                     attrs={'autocomplete': 'off'},

                                 ))
    end_date = forms.DateField(input_formats=['%Y-%m-%d'],
                                 label='Data rozpoczęcia:',
                                 widget=FengyuanChenDatePickerInput(
                                     attrs={'autocomplete': 'off'},
                                 ))

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['originator', 'applied', 'comment', 'verified', 'votes']


class AddCostForm(forms.ModelForm):
    originator_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Cost
        fields = '__all__'
        exclude = ('whole_cost', 'originator')
        widgets = {
            'grant_cost': forms.NumberInput(attrs={'step': '0.01'}),
            'other_cost': forms.NumberInput(attrs={'step': '0.01'}),
        }


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label='Uwagi', required=False)
    verified = forms.IntegerField(widget=forms.Select(choices=VERIFIED), label='Weryfikacja formalna:', required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło', max_length=64)


class VoteForm(forms.ModelForm):
    pesel = forms.CharField(validators=[validate_pesel], widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    phone = forms.IntegerField(label='Numer telefonu', validators=[validate_phone])
    sport_project = forms.ModelChoiceField(label='Projekt sportowy', queryset=Project.objects.filter(
        applied=True, verified=1, subject=1), empty_label='wybierz projekt', required=False)
    tourist_project = forms.ModelChoiceField(label='Projekt turystyczny', queryset=Project.objects.filter(
        applied=True, verified=1, subject=2), empty_label='wybierz projekt', required=False)
    cultural_project = forms.ModelChoiceField(label='Projekt kulturalny', queryset=Project.objects.filter(
        applied=True, verified=1, subject=3), empty_label='wybierz projekt', required=False)
    disabled_project = forms.ModelChoiceField(label='Projekt sportowy', queryset=Project.objects.filter(
        applied=True, verified=1, subject=4), empty_label='wybierz projekt', required=False)
    civil_society_project = forms.ModelChoiceField(label='Projekt sportowy', queryset=Project.objects.filter(
        applied=True, verified=1, subject=5), empty_label='wybierz projekt', required=False)
    seniors_project = forms.ModelChoiceField(label='Projekt sportowy', queryset=Project.objects.filter(
        applied=True, verified=1, subject=6), empty_label='wybierz projekt', required=False)
    craft_project = forms.ModelChoiceField(label='Projekt sportowy', queryset=Project.objects.filter(
        applied=True, verified=1, subject=7), empty_label='wybierz projekt', required=False)

    class Meta:
        model = Voter
        fields = '__all__'

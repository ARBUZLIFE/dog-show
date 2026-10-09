import re
from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import (
    Dog, Club, Breed, Owner,
    Ring, Expert, Medal, RingBreedSchedule,
)

class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault('class', 'form-select')
            else:
                widget.attrs.setdefault('class', 'form-control')


class DogForm(BootstrapModelForm):

    pedigree_series = forms.CharField(
        label='Серия родословной',
        max_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': '001',
            'inputmode': 'numeric',
            'autocomplete': 'off',
        }),
        help_text='Три цифры серии, например 001.',
    )
    pedigree_year = forms.CharField(
        label='Год родословной',
        max_length=4,
        widget=forms.TextInput(attrs={
            'placeholder': '2020',
            'inputmode': 'numeric',
            'autocomplete': 'off',
        }),
        help_text='Четыре цифры года, например 2020.',
    )

    class Meta:
        model = Dog
        fields = [
            'name', 'breed', 'club', 'owner', 'age',
            'parent_names',
            'last_vaccination_date', 'is_disqualified',
        ]
        widgets = {
            'last_vaccination_date': forms.DateInput(attrs={'type': 'date'}),
            'age': forms.NumberInput(attrs={'min': 1, 'max': 30}),
        }
        labels = {
            'name': 'Кличка',
            'breed': 'Порода',
            'club': 'Клуб',
            'owner': 'Хозяин',
            'age': 'Возраст (лет)',
            'parent_names': 'Клички родителей',
            'last_vaccination_date': 'Дата последней прививки',
            'is_disqualified': 'Отстранена от участия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.pedigree_number:
            match = re.match(r'^РКФ-(\d{3})-(\d{4})$', self.instance.pedigree_number)
            if match:
                self.fields['pedigree_series'].initial = match.group(1)
                self.fields['pedigree_year'].initial = match.group(2)
        ordered = [
            'name', 'breed', 'club', 'owner', 'age',
            'pedigree_series', 'pedigree_year',
            'parent_names', 'last_vaccination_date', 'is_disqualified',
        ]
        self.order_fields(ordered)

    def clean_pedigree_series(self):
        series = (self.cleaned_data.get('pedigree_series') or '').strip()
        if not series.isdigit():
            raise ValidationError('Серия должна содержать только цифры.')
        if len(series) != 3:
            raise ValidationError('Серия должна состоять ровно из 3 цифр.')
        return series

    def clean_pedigree_year(self):
        year = (self.cleaned_data.get('pedigree_year') or '').strip()
        if not year.isdigit():
            raise ValidationError('Год должен содержать только цифры.')
        if len(year) != 4:
            raise ValidationError('Год должен состоять ровно из 4 цифр.')
        return year

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            raise ValidationError('Укажите возраст.')
        if age < 1:
            raise ValidationError('Возраст должен быть не меньше 1 года.')
        if age > 30:
            raise ValidationError('Возраст не может быть больше 30 лет.')
        return age

    def clean_last_vaccination_date(self):
        vd = self.cleaned_data.get('last_vaccination_date')
        if vd and vd > date.today():
            raise ValidationError('Дата прививки не может быть в будущем.')
        return vd

    def clean(self):
        cleaned = super().clean()
        series = cleaned.get('pedigree_series')
        year = cleaned.get('pedigree_year')

        if series and year:
            full_number = f'РКФ-{series}-{year}'
            qs = Dog.objects.filter(pedigree_number=full_number)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error(
                    'pedigree_series',
                    f'Собака с номером {full_number} уже существует.'
                )
        return cleaned

    def save(self, commit=True):
        dog = super().save(commit=False)
        series = self.cleaned_data.get('pedigree_series')
        year = self.cleaned_data.get('pedigree_year')
        if series and year:
            dog.pedigree_number = f'РКФ-{series}-{year}'
        if commit:
            dog.save()
            self.save_m2m()
        return dog


class ClubForm(BootstrapModelForm):
    class Meta:
        model = Club
        fields = ['name']
        labels = {'name': 'Название клуба'}


class BreedForm(BootstrapModelForm):
    class Meta:
        model = Breed
        fields = ['name']
        labels = {'name': 'Название породы'}


class OwnerForm(BootstrapModelForm):
    class Meta:
        model = Owner
        fields = ['full_name', 'passport_data']
        labels = {
            'full_name': 'ФИО',
            'passport_data': 'Паспортные данные',
        }


class RingForm(BootstrapModelForm):
    class Meta:
        model = Ring
        fields = ['number', 'address', 'club']
        labels = {
            'number': 'Номер ринга',
            'address': 'Адрес',
            'club': 'Клуб',
        }


class ExpertForm(BootstrapModelForm):
    class Meta:
        model = Expert
        fields = ['full_name', 'breed', 'ring', 'club', 'is_active']
        labels = {
            'full_name': 'ФИО',
            'breed': 'Специализация (порода)',
            'ring': 'Ринг',
            'club': 'Клуб',
            'is_active': 'Активен',
        }

    def clean(self):
        cleaned = super().clean()
        club = cleaned.get('club')
        ring = cleaned.get('ring')
        if club and ring and ring.club_id != club.id:
            raise ValidationError(
                'Выбранный ринг принадлежит другому клубу.'
            )
        return cleaned


class MedalForm(BootstrapModelForm):
    class Meta:
        model = Medal
        fields = ['dog', 'medal_type', 'awarded_at']
        widgets = {
            'awarded_at': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'dog': 'Собака',
            'medal_type': 'Тип медали',
            'awarded_at': 'Дата награждения',
        }


class ScheduleForm(BootstrapModelForm):
    class Meta:
        model = RingBreedSchedule
        fields = ['ring', 'breed', 'time_slot']
        labels = {
            'ring': 'Ринг',
            'breed': 'Порода',
            'time_slot': 'Временной слот',
        }
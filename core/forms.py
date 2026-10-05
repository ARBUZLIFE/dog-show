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

    class Meta:
        model = Dog
        fields = [
            'name', 'breed', 'club', 'owner', 'age',
            'pedigree_number', 'parent_names',
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
            'pedigree_number': 'Номер родословной',
            'parent_names': 'Клички родителей',
            'last_vaccination_date': 'Дата последней прививки',
            'is_disqualified': 'Отстранена от участия',
        }

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

    def clean_pedigree_number(self):
        number = self.cleaned_data.get('pedigree_number')
        qs = Dog.objects.filter(pedigree_number=number)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Собака с таким номером родословной уже существует.')
        return number


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
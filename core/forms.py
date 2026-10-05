from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import Dog


class DogForm(forms.ModelForm):

    class Meta:
        model = Dog
        fields = [
            'name', 'breed', 'club', 'owner', 'age',
            'pedigree_number', 'parent_names',
            'last_vaccination_date', 'is_disqualified',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'club': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'pedigree_number': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_names': forms.TextInput(attrs={'class': 'form-control'}),
            'last_vaccination_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'is_disqualified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
        """Проверка возраста."""
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
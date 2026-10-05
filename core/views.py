from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import (
    Dog, Club, Breed, Owner,
    Ring, Expert, Medal, RingBreedSchedule,
)
from .forms import (
    DogForm, ClubForm, BreedForm, OwnerForm,
    RingForm, ExpertForm, MedalForm, ScheduleForm,
)


# Базовые классы с уведомлениями

class MessageCreateView(LoginRequiredMixin, CreateView):
    cancel_url = None

    def form_valid(self, form):
        messages.success(self.request, self.get_success_message(form.instance))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_message(self, obj):
        return f'Объект «{obj}» создан.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Добавить: {self.model._meta.verbose_name}'
        ctx['button_label'] = 'Создать'
        ctx['cancel_url'] = self.cancel_url
        return ctx


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    cancel_url = None

    def form_valid(self, form):
        messages.success(self.request, self.get_success_message(form.instance))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_message(self, obj):
        return f'Объект «{obj}» обновлён.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Редактировать: {self.object}'
        ctx['button_label'] = 'Сохранить'
        ctx['cancel_url'] = self.cancel_url
        return ctx


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    cancel_url = None
    delete_warning = ''

    def form_valid(self, form):
        messages.success(self.request, self.get_success_message(self.object))
        return super().form_valid(form)

    def get_success_message(self, obj):
        return f'Объект «{obj}» удалён.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = self.cancel_url
        ctx['delete_warning'] = self.delete_warning
        return ctx


# Главная

def home(request):
    return render(request, 'home.html')


# Каталог
def catalog(request):
    return render(request, 'core/catalog.html')

def catalog_participants(request):
    """Хаб: Участники."""
    return render(request, 'core/catalog_participants.html')

def catalog_exhibitions(request):
    """Хаб: Эксперты и ринги."""
    return render(request, 'core/catalog_exhibitions.html')


# Собаки

class DogListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'core/dog_list.html'
    context_object_name = 'dogs'

    def get_queryset(self):
        return Dog.objects.select_related('breed', 'club', 'owner')


class DogCreateView(MessageCreateView):
    model = Dog
    form_class = DogForm
    template_name = 'core/dog_form.html'
    success_url = reverse_lazy('dog_list')

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» успешно добавлена.'


class DogUpdateView(MessageUpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'core/dog_form.html'
    success_url = reverse_lazy('dog_list')

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» обновлена.'


class DogDeleteView(MessageDeleteView):
    model = Dog
    template_name = 'core/dog_confirm_delete.html'
    success_url = reverse_lazy('dog_list')

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» удалена.'


# Клубы

class ClubListView(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'core/club_list.html'
    context_object_name = 'clubs'


class ClubCreateView(MessageCreateView):
    model = Club
    form_class = ClubForm
    template_name = 'core/club_form.html'
    success_url = reverse_lazy('club_list')

    def get_success_message(self, obj):
        return f'Клуб «{obj.name}» добавлен.'


class ClubUpdateView(MessageUpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'core/club_form.html'
    success_url = reverse_lazy('club_list')

    def get_success_message(self, obj):
        return f'Клуб «{obj.name}» обновлён.'


class ClubDeleteView(MessageDeleteView):
    model = Club
    template_name = 'core/club_confirm_delete.html'
    success_url = reverse_lazy('club_list')

    def get_success_message(self, obj):
        return f'Клуб «{obj.name}» удалён.'


# Породы

class BreedListView(LoginRequiredMixin, ListView):
    model = Breed
    template_name = 'core/breed_list.html'
    context_object_name = 'breeds'


class BreedCreateView(MessageCreateView):
    model = Breed
    form_class = BreedForm
    template_name = 'core/breed_form.html'
    success_url = reverse_lazy('breed_list')

    def get_success_message(self, obj):
        return f'Порода «{obj.name}» добавлена.'


class BreedUpdateView(MessageUpdateView):
    model = Breed
    form_class = BreedForm
    template_name = 'core/breed_form.html'
    success_url = reverse_lazy('breed_list')

    def get_success_message(self, obj):
        return f'Порода «{obj.name}» обновлена.'


class BreedDeleteView(MessageDeleteView):
    model = Breed
    template_name = 'core/breed_confirm_delete.html'
    success_url = reverse_lazy('breed_list')

    def get_success_message(self, obj):
        return f'Порода «{obj.name}» удалена.'


# Хозяева

class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner
    template_name = 'core/owner_list.html'
    context_object_name = 'owners'


class OwnerCreateView(MessageCreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'core/owner_form.html'
    success_url = reverse_lazy('owner_list')

    def get_success_message(self, obj):
        return f'Хозяин «{obj.full_name}» добавлен.'


class OwnerUpdateView(MessageUpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'core/owner_form.html'
    success_url = reverse_lazy('owner_list')

    def get_success_message(self, obj):
        return f'Хозяин «{obj.full_name}» обновлён.'


class OwnerDeleteView(MessageDeleteView):
    model = Owner
    template_name = 'core/owner_confirm_delete.html'
    success_url = reverse_lazy('owner_list')

    def get_success_message(self, obj):
        return f'Хозяин «{obj.full_name}» удалён.'


# Ринги

class RingListView(LoginRequiredMixin, ListView):
    model = Ring
    template_name = 'core/generic_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Ring.objects.select_related('club')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'list_title': 'Ринги',
            'list_icon': 'bi-geo-alt',
            'create_url': 'ring_create',
            'create_label': 'Добавить ринг',
            'empty_message': 'Пока нет ни одного ринга.',
            'update_url_name': 'ring_update',
            'delete_url_name': 'ring_delete',
            'columns': [
                {'label': 'Номер', 'attr': 'number', 'style': 'strong'},
                {'label': 'Адрес', 'attr': 'address'},
                {'label': 'Клуб', 'attr': 'club.name'},
            ],
        })
        return ctx


class RingCreateView(MessageCreateView):
    model = Ring
    form_class = RingForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('ring_list')
    cancel_url = 'ring_list'

    def get_success_message(self, obj):
        return f'Ринг №{obj.number} добавлен.'


class RingUpdateView(MessageUpdateView):
    model = Ring
    form_class = RingForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('ring_list')
    cancel_url = 'ring_list'

    def get_success_message(self, obj):
        return f'Ринг №{obj.number} обновлён.'


class RingDeleteView(MessageDeleteView):
    model = Ring
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('ring_list')
    cancel_url = 'ring_list'
    delete_warning = 'Внимание: связанные расписания и эксперты также будут затронуты.'

    def get_success_message(self, obj):
        return f'Ринг №{obj.number} удалён.'


# Эксперты

class ExpertListView(LoginRequiredMixin, ListView):
    model = Expert
    template_name = 'core/generic_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Expert.objects.select_related('breed', 'ring', 'club')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'list_title': 'Эксперты',
            'list_icon': 'bi-person-workspace',
            'create_url': 'expert_create',
            'create_label': 'Добавить эксперта',
            'empty_message': 'Пока нет ни одного эксперта.',
            'update_url_name': 'expert_update',
            'delete_url_name': 'expert_delete',
            'columns': [
                {'label': 'ФИО', 'attr': 'full_name', 'style': 'strong'},
                {'label': 'Специализация', 'attr': 'breed.name'},
                {'label': 'Ринг', 'attr': 'ring.number'},
                {'label': 'Клуб', 'attr': 'club.name'},
                {'label': 'Статус', 'attr': 'is_active', 'style': 'boolean'},
            ],
        })
        return ctx


class ExpertCreateView(MessageCreateView):
    model = Expert
    form_class = ExpertForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('expert_list')
    cancel_url = 'expert_list'

    def get_success_message(self, obj):
        return f'Эксперт «{obj.full_name}» добавлен.'


class ExpertUpdateView(MessageUpdateView):
    model = Expert
    form_class = ExpertForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('expert_list')
    cancel_url = 'expert_list'

    def get_success_message(self, obj):
        return f'Эксперт «{obj.full_name}» обновлён.'


class ExpertDeleteView(MessageDeleteView):
    model = Expert
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('expert_list')
    cancel_url = 'expert_list'

    def get_success_message(self, obj):
        return f'Эксперт «{obj.full_name}» удалён.'


# Медали

class MedalListView(LoginRequiredMixin, ListView):
    model = Medal
    template_name = 'core/generic_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Medal.objects.select_related('dog', 'breed')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'list_title': 'Медали',
            'list_icon': 'bi-award',
            'create_url': 'medal_create',
            'create_label': 'Добавить медаль',
            'empty_message': 'Пока нет ни одной медали.',
            'update_url_name': 'medal_update',
            'delete_url_name': 'medal_delete',
            'columns': [
                {'label': 'Собака', 'attr': 'dog.name', 'style': 'strong'},
                {'label': 'Порода', 'attr': 'breed.name'},
                {'label': 'Тип', 'attr': 'get_medal_type_display', 'style': 'medal_badge'},
                {'label': 'Дата', 'attr': 'awarded_at', 'style': 'date'},
            ],
        })
        return ctx


class MedalCreateView(MessageCreateView):
    model = Medal
    form_class = MedalForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('medal_list')
    cancel_url = 'medal_list'

    def get_success_message(self, obj):
        return f'Медаль для «{obj.dog.name}» добавлена.'


class MedalUpdateView(MessageUpdateView):
    model = Medal
    form_class = MedalForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('medal_list')
    cancel_url = 'medal_list'

    def get_success_message(self, obj):
        return f'Медаль обновлена.'


class MedalDeleteView(MessageDeleteView):
    model = Medal
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('medal_list')
    cancel_url = 'medal_list'

    def get_success_message(self, obj):
        return f'Медаль удалена.'


# Расписания

class ScheduleListView(LoginRequiredMixin, ListView):
    model = RingBreedSchedule
    template_name = 'core/generic_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return RingBreedSchedule.objects.select_related('ring', 'breed')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'list_title': 'Расписания рингов',
            'list_icon': 'bi-calendar-week',
            'create_url': 'schedule_create',
            'create_label': 'Добавить слот',
            'empty_message': 'Пока нет ни одного слота расписания.',
            'update_url_name': 'schedule_update',
            'delete_url_name': 'schedule_delete',
            'columns': [
                {'label': 'Ринг', 'attr': 'ring.number'},
                {'label': 'Порода', 'attr': 'breed.name', 'style': 'strong'},
                {'label': 'Слот', 'attr': 'time_slot'},
            ],
        })
        return ctx


class ScheduleCreateView(MessageCreateView):
    model = RingBreedSchedule
    form_class = ScheduleForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('schedule_list')
    cancel_url = 'schedule_list'

    def get_success_message(self, obj):
        return f'Слот добавлен: {obj}'


class ScheduleUpdateView(MessageUpdateView):
    model = RingBreedSchedule
    form_class = ScheduleForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('schedule_list')
    cancel_url = 'schedule_list'

    def get_success_message(self, obj):
        return f'Слот обновлён: {obj}'


class ScheduleDeleteView(MessageDeleteView):
    model = RingBreedSchedule
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')
    cancel_url = 'schedule_list'

    def get_success_message(self, obj):
        return f'Слот удалён.'
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views import View
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView,
)

from .models import (
    Dog, Club, Breed, Owner,
    Ring, Expert, Medal, RingBreedSchedule,
)
from .forms import (
    DogForm, ClubForm, BreedForm, OwnerForm,
    RingForm, ExpertForm, MedalForm, ScheduleForm,
)


# БАЗОВЫЕ КЛАССЫ

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


class MessageListView(LoginRequiredMixin, ListView):
    template_name = 'core/generic_list.html'
    context_object_name = 'objects'

    detail_url_name = None
    list_title = ''
    list_icon = ''
    create_url = None
    create_label = 'Добавить'
    empty_message = 'Пока ничего нет.'
    update_url_name = None
    delete_url_name = None
    columns = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'detail_url_name': self.detail_url_name,
            'list_title': self.list_title,
            'list_icon': self.list_icon,
            'create_url': self.create_url,
            'create_label': self.create_label,
            'empty_message': self.empty_message,
            'update_url_name': self.update_url_name,
            'delete_url_name': self.delete_url_name,
            'columns': self.columns,
        })
        return ctx


class MessageDetailView(LoginRequiredMixin, DetailView):
    template_name = 'core/generic_detail.html'
    context_object_name = 'object'

    detail_title = ''
    detail_icon = ''
    update_url_name = None
    delete_url_name = None
    list_url_name = None
    breadcrumbs = []

    def get_detail_title(self):
        return self.detail_title or str(self.object)

    def get_info_rows(self):
        return []

    def get_related_sections(self):
        return []

    def get_extra_actions(self):
        return []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'detail_title': self.get_detail_title(),
            'detail_icon': self.detail_icon,
            'update_url_name': self.update_url_name,
            'delete_url_name': self.delete_url_name,
            'list_url_name': self.list_url_name,
            'breadcrumbs': self.breadcrumbs,
            'info_rows': self.get_info_rows(),
            'related_sections': self.get_related_sections(),
            'extra_actions': self.get_extra_actions(),
        })
        return ctx


def row(label, value, link=None, strong=False, code=False, muted=False, badge=None):
    return {
        'label': label,
        'value': value,
        'link': link,
        'strong': strong,
        'code': code,
        'muted': muted,
        'badge': badge,
    }


# ГЛАВНАЯ И КАТАЛОГИ

def home(request):
    return render(request, 'home.html')


def catalog(request):
    return render(request, 'core/catalog.html')


def catalog_participants(request):
    return render(request, 'core/catalog_participants.html')


def catalog_exhibitions(request):
    return render(request, 'core/catalog_exhibitions.html')


def catalog_medals(request):
    return render(request, 'core/catalog_medals.html')


# СОБАКИ

class DogListView(MessageListView):
    model = Dog
    list_title = 'Собаки'
    list_icon = 'bi-clipboard-check'
    create_url = 'dog_create'
    create_label = 'Добавить собаку'
    empty_message = 'Пока нет ни одной собаки.'
    update_url_name = 'dog_update'
    delete_url_name = 'dog_delete'
    detail_url_name = 'dog_detail'
    columns = [
        {'label': 'Кличка', 'attr': 'name', 'style': 'strong'},
        {'label': 'Порода', 'attr': 'breed.name'},
        {'label': 'Клуб', 'attr': 'club.name'},
        {'label': 'Хозяин', 'attr': 'owner.full_name'},
        {'label': 'Возраст', 'attr': 'age'},
        {'label': '№ родословной', 'attr': 'pedigree_number', 'style': 'code'},
        {'label': 'Статус', 'attr': 'is_disqualified', 'style': 'bool_badge',
         'true_label': 'Отстранена', 'true_color': 'danger',
         'false_label': 'Участвует', 'false_color': 'success'},
    ]

    def get_queryset(self):
        return Dog.objects.select_related('breed', 'club', 'owner')


class DogCreateView(MessageCreateView):
    model = Dog
    form_class = DogForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('dog_list')
    cancel_url = 'dog_list'

    def get_initial(self):
        initial = super().get_initial()
        club_id = self.request.GET.get('club')
        if club_id:
            initial['club'] = club_id
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        club_id = self.request.GET.get('club')
        if club_id:
            try:
                club = Club.objects.get(pk=club_id)
                ctx['form_note'] = f'Собака будет принята в клуб «{club.name}».'
                ctx['cancel_url_explicit'] = reverse('club_detail', args=[club.pk])
            except Club.DoesNotExist:
                pass
        return ctx

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» успешно добавлена.'


class DogUpdateView(MessageUpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('dog_list')
    cancel_url = 'dog_list'

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» обновлена.'


class DogDeleteView(MessageDeleteView):
    model = Dog
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('dog_list')
    cancel_url = 'dog_list'
    delete_warning = 'Внимание: связанные медали также будут удалены.'

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» удалена.'


class DogDetailView(MessageDetailView):
    model = Dog
    detail_icon = 'bi-clipboard-check'
    update_url_name = 'dog_update'
    delete_url_name = 'dog_delete'
    list_url_name = 'dog_list'

    def get_detail_title(self):
        return f'Собака: {self.object.name}'

    def get_extra_actions(self):
        dog = self.object
        if dog.is_disqualified:
            return [{
                'label': 'Восстановить',
                'url': reverse('dog_restore', args=[dog.pk]),
                'icon': 'bi-check-circle',
                'style': 'outline-success',
            }]
        return [{
            'label': 'Отстранить',
            'url': reverse('dog_disqualify', args=[dog.pk]),
            'icon': 'bi-x-octagon',
            'style': 'outline-warning',
        }]

    def get_info_rows(self):
        dog = self.object
        return [
            row('Кличка', dog.name, strong=True),
            row('Порода', dog.breed.name, link=reverse('breed_detail', args=[dog.breed.pk])),
            row('Клуб', dog.club.name, link=reverse('club_detail', args=[dog.club.pk])),
            row('Хозяин', dog.owner.full_name, link=reverse('owner_detail', args=[dog.owner.pk])),
            row('Возраст', f'{dog.age} лет'),
            row('№ родословной', dog.pedigree_number, code=True),
            row('Родители', dog.parent_names),
            row('Дата прививки', dog.last_vaccination_date.strftime('%d.%m.%Y')),
            row('Статус',
                'Отстранена' if dog.is_disqualified else 'Участвует',
                badge='danger' if dog.is_disqualified else 'success'),
        ]

    def get_related_sections(self):
        dog = self.object
        sections = [
            {
                'title': 'Медали собаки',
                'icon': 'bi-award',
                'items': dog.medals.select_related('breed'),
                'item_url_name': 'medal_detail',
                'columns': [
                    {'label': 'Тип', 'attr': 'get_medal_type_display', 'style': 'medal_badge'},
                    {'label': 'Порода', 'attr': 'breed.name'},
                    {'label': 'Дата', 'attr': 'awarded_at', 'style': 'date'},
                ],
                'empty_message': 'Собака не получала медалей.',
            },
        ]

        schedule = dog.breed.schedule.select_related('ring', 'ring__club')
        if schedule.exists():
            sections.append({
                'title': 'Расписание показа',
                'icon': 'bi-calendar-week',
                'items': schedule,
                'item_url_name': 'schedule_detail',
                'columns': [
                    {'label': 'Ринг', 'attr': 'ring.number'},
                    {'label': 'Клуб', 'attr': 'ring.club.name'},
                    {'label': 'Адрес', 'attr': 'ring.address'},
                    {'label': 'Время', 'attr': 'time_slot', 'style': 'strong'},
                ],
                'empty_message': 'Для этой породы не назначено ринга.',
            })

        return sections

# КЛУБЫ

class ClubListView(MessageListView):
    model = Club
    list_title = 'Клубы'
    list_icon = 'bi-diagram-3'
    create_url = 'club_create'
    create_label = 'Добавить клуб'
    empty_message = 'Пока нет ни одного клуба.'
    update_url_name = 'club_update'
    delete_url_name = 'club_delete'
    detail_url_name = 'club_detail'
    columns = [
        {'label': 'Название', 'attr': 'name', 'style': 'strong'},
        {'label': 'Дата создания', 'attr': 'created_at', 'style': 'datetime'},
    ]


class ClubCreateView(MessageCreateView):
    model = Club
    form_class = ClubForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('club_list')
    cancel_url = 'club_list'

    def get_success_message(self, obj):
        return f'Клуб «{obj.name}» добавлен.'


class ClubUpdateView(MessageUpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('club_list')
    cancel_url = 'club_list'

    def get_success_message(self, obj):
        return f'Клуб «{obj.name}» обновлён.'


class ClubDeleteView(MessageDeleteView):
    model = Club
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('club_list')
    cancel_url = 'club_list'
    delete_warning = 'Внимание: связанные ринги, собаки и эксперты также будут затронуты.'

    def get_success_message(self, obj):
        return f'Клуб «{obj.name}» удалён.'


class ClubDetailView(MessageDetailView):
    model = Club
    detail_icon = 'bi-diagram-3'
    update_url_name = 'club_update'
    delete_url_name = 'club_delete'
    list_url_name = 'club_list'

    def get_detail_title(self):
        return f'Клуб: {self.object.name}'

    def get_extra_actions(self):
        club = self.object
        return [
            {
                'label': 'Принять собаку',
                'url': reverse('dog_create') + f'?club={club.pk}',
                'icon': 'bi-plus-circle',
                'style': 'outline-primary',
            },
            {
                'label': 'Принять эксперта',
                'url': reverse('expert_create') + f'?club={club.pk}',
                'icon': 'bi-plus-circle',
                'style': 'outline-primary',
            },
        ]

    def get_info_rows(self):
        club = self.object
        return [
            row('Название', club.name, strong=True),
            row('Дата создания', club.created_at.strftime('%d.%m.%Y %H:%M')),
        ]

    def get_related_sections(self):
        club = self.object

        breeds = (
            Breed.objects
            .filter(dogs__club=club)
            .distinct()
            .order_by('name')
        )
        breeds_with_count = [
            {'breed': b, 'dog_count': Dog.objects.filter(club=club, breed=b).count()}
            for b in breeds
        ]

        medal_qs = Medal.objects.filter(dog__club=club).values('medal_type')
        medal_counts = defaultdict(int)
        for m in medal_qs:
            medal_counts[m['medal_type']] += 1
        medal_total = sum(medal_counts.values())
        medal_summary = {
            'gold': medal_counts.get('gold', 0),
            'silver': medal_counts.get('silver', 0),
            'bronze': medal_counts.get('bronze', 0),
            'total': medal_total,
        }

        return [
            {
                'title': 'Ринги клуба',
                'icon': 'bi-geo-alt',
                'items': club.rings.all(),
                'item_url_name': 'ring_detail',
                'columns': [
                    {'label': 'Номер', 'attr': 'number', 'style': 'strong'},
                    {'label': 'Адрес', 'attr': 'address'},
                ],
                'empty_message': 'У клуба нет рингов.',
            },
            {
                'title': 'Собаки клуба',
                'icon': 'bi-clipboard-check',
                'items': club.dogs.select_related('breed', 'owner'),
                'item_url_name': 'dog_detail',
                'columns': [
                    {'label': 'Кличка', 'attr': 'name', 'style': 'strong'},
                    {'label': 'Порода', 'attr': 'breed.name'},
                    {'label': 'Хозяин', 'attr': 'owner.full_name'},
                ],
                'empty_message': 'В клубе нет собак.',
            },
            {
                'title': 'Эксперты клуба',
                'icon': 'bi-person-workspace',
                'items': club.experts.select_related('breed', 'ring'),
                'item_url_name': 'expert_detail',
                'columns': [
                    {'label': 'ФИО', 'attr': 'full_name', 'style': 'strong'},
                    {'label': 'Специализация', 'attr': 'breed.name'},
                    {'label': 'Статус', 'attr': 'is_active', 'style': 'bool_badge',
                     'true_label': 'Активен', 'true_color': 'success',
                     'false_label': 'Уволен', 'false_color': 'secondary'},
                ],
                'empty_message': 'В клубе нет экспертов.',
            },
            {
                'title': 'Породы клуба',
                'icon': 'bi-tags',
                'items': breeds_with_count,
                'item_url_name': None,
                'custom_template': 'core/_breed_summary_table.html',
                'empty_message': 'У клуба нет собак — породы не определены.',
            },
            {
                'title': 'Медали клуба',
                'icon': 'bi-award',
                'items': [],
                'custom_template': 'core/_club_medals_summary.html',
                'medal_summary': medal_summary,
                'empty_message': 'У собак этого клуба нет медалей.',
            },
        ]

# ПОРОДЫ

class BreedListView(MessageListView):
    model = Breed
    list_title = 'Породы'
    list_icon = 'bi-tags'
    create_url = 'breed_create'
    create_label = 'Добавить породу'
    empty_message = 'Пока нет ни одной породы.'
    update_url_name = 'breed_update'
    delete_url_name = 'breed_delete'
    detail_url_name = 'breed_detail'
    columns = [
        {'label': 'Название', 'attr': 'name', 'style': 'strong'},
    ]


class BreedCreateView(MessageCreateView):
    model = Breed
    form_class = BreedForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('breed_list')
    cancel_url = 'breed_list'

    def get_success_message(self, obj):
        return f'Порода «{obj.name}» добавлена.'


class BreedUpdateView(MessageUpdateView):
    model = Breed
    form_class = BreedForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('breed_list')
    cancel_url = 'breed_list'

    def get_success_message(self, obj):
        return f'Порода «{obj.name}» обновлена.'


class BreedDeleteView(MessageDeleteView):
    model = Breed
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('breed_list')
    cancel_url = 'breed_list'
    delete_warning = 'Внимание: связанные собаки, эксперты и медали также будут затронуты.'

    def get_success_message(self, obj):
        return f'Порода «{obj.name}» удалена.'


class BreedDetailView(MessageDetailView):
    model = Breed
    detail_icon = 'bi-tags'
    update_url_name = 'breed_update'
    delete_url_name = 'breed_delete'
    list_url_name = 'breed_list'

    def get_detail_title(self):
        return f'Порода: {self.object.name}'

    def get_info_rows(self):
        return [row('Название', self.object.name, strong=True)]

    def get_related_sections(self):
        breed = self.object
        return [
            {
                'title': 'Собаки этой породы',
                'icon': 'bi-clipboard-check',
                'items': breed.dogs.select_related('club', 'owner'),
                'item_url_name': 'dog_detail',
                'columns': [
                    {'label': 'Кличка', 'attr': 'name', 'style': 'strong'},
                    {'label': 'Клуб', 'attr': 'club.name'},
                    {'label': 'Хозяин', 'attr': 'owner.full_name'},
                    {'label': 'Возраст', 'attr': 'age'},
                ],
                'empty_message': 'Собак этой породы нет.',
            },
            {
                'title': 'Эксперты по породе',
                'icon': 'bi-person-workspace',
                'items': breed.experts.select_related('ring', 'club'),
                'item_url_name': 'expert_detail',
                'columns': [
                    {'label': 'ФИО', 'attr': 'full_name', 'style': 'strong'},
                    {'label': 'Ринг', 'attr': 'ring.number'},
                    {'label': 'Клуб', 'attr': 'club.name'},
                ],
                'empty_message': 'По этой породе нет экспертов.',
            },
            {
                'title': 'Медали по породе',
                'icon': 'bi-award',
                'items': breed.medals.select_related('dog'),
                'item_url_name': 'medal_detail',
                'columns': [
                    {'label': 'Собака', 'attr': 'dog.name', 'style': 'strong'},
                    {'label': 'Тип', 'attr': 'get_medal_type_display', 'style': 'medal_badge'},
                    {'label': 'Дата', 'attr': 'awarded_at', 'style': 'date'},
                ],
                'empty_message': 'По этой породе ещё нет медалей.',
            },
            {
                'title': 'Расписание показов',
                'icon': 'bi-calendar-week',
                'items': breed.schedule.select_related('ring'),
                'item_url_name': 'schedule_detail',
                'columns': [
                    {'label': 'Ринг', 'attr': 'ring.number'},
                    {'label': 'Слот', 'attr': 'time_slot'},
                ],
                'empty_message': 'Порода не включена в расписание.',
            },
        ]


# ХОЗЯЕВА

class OwnerListView(MessageListView):
    model = Owner
    list_title = 'Хозяева'
    list_icon = 'bi-person-badge'
    create_url = 'owner_create'
    create_label = 'Добавить хозяина'
    empty_message = 'Пока нет ни одного хозяина.'
    update_url_name = 'owner_update'
    delete_url_name = 'owner_delete'
    detail_url_name = 'owner_detail'
    columns = [
        {'label': 'ФИО', 'attr': 'full_name', 'style': 'strong'},
        {'label': 'Паспортные данные', 'attr': 'passport_data', 'style': 'code'},
    ]


class OwnerCreateView(MessageCreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('owner_list')
    cancel_url = 'owner_list'

    def get_success_message(self, obj):
        return f'Хозяин «{obj.full_name}» добавлен.'


class OwnerUpdateView(MessageUpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('owner_list')
    cancel_url = 'owner_list'

    def get_success_message(self, obj):
        return f'Хозяин «{obj.full_name}» обновлён.'


class OwnerDeleteView(MessageDeleteView):
    model = Owner
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('owner_list')
    cancel_url = 'owner_list'
    delete_warning = 'Внимание: у хозяина могут быть собаки — они тоже будут затронуты.'

    def get_success_message(self, obj):
        return f'Хозяин «{obj.full_name}» удалён.'


class OwnerDetailView(MessageDetailView):
    model = Owner
    detail_icon = 'bi-person-badge'
    update_url_name = 'owner_update'
    delete_url_name = 'owner_delete'
    list_url_name = 'owner_list'

    def get_detail_title(self):
        return f'Хозяин: {self.object.full_name}'

    def get_info_rows(self):
        owner = self.object
        return [
            row('ФИО', owner.full_name, strong=True),
            row('Паспортные данные', owner.passport_data, code=True),
        ]

    def get_related_sections(self):
        owner = self.object
        return [
            {
                'title': 'Собаки хозяина',
                'icon': 'bi-clipboard-check',
                'items': owner.dogs.select_related('breed', 'club'),
                'item_url_name': 'dog_detail',
                'columns': [
                    {'label': 'Кличка', 'attr': 'name', 'style': 'strong'},
                    {'label': 'Порода', 'attr': 'breed.name'},
                    {'label': 'Клуб', 'attr': 'club.name'},
                    {'label': 'Возраст', 'attr': 'age'},
                ],
                'empty_message': 'У хозяина нет собак.',
            },
        ]


# РИНГИ

class RingListView(MessageListView):
    model = Ring
    list_title = 'Ринги'
    list_icon = 'bi-geo-alt'
    create_url = 'ring_create'
    create_label = 'Добавить ринг'
    empty_message = 'Пока нет ни одного ринга.'
    update_url_name = 'ring_update'
    delete_url_name = 'ring_delete'
    detail_url_name = 'ring_detail'
    columns = [
        {'label': 'Номер', 'attr': 'number', 'style': 'strong'},
        {'label': 'Адрес', 'attr': 'address'},
        {'label': 'Клуб', 'attr': 'club.name'},
        {'label': 'Расписание', 'attr': 'get_schedule_summary'},
    ]

    def get_queryset(self):
        return Ring.objects.select_related('club')


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


class RingDetailView(MessageDetailView):
    model = Ring
    detail_icon = 'bi-geo-alt'
    update_url_name = 'ring_update'
    delete_url_name = 'ring_delete'
    list_url_name = 'ring_list'

    def get_detail_title(self):
        return f'Ринг №{self.object.number}'

    def get_info_rows(self):
        ring = self.object
        return [
            row('Номер', ring.number, strong=True),
            row('Адрес', ring.address),
            row('Клуб', ring.club.name, link=reverse('club_detail', args=[ring.club.pk])),
        ]

    def get_related_sections(self):
        ring = self.object
        return [
            {
                'title': 'Эксперты ринга',
                'icon': 'bi-person-workspace',
                'items': ring.experts.select_related('breed', 'club'),
                'item_url_name': 'expert_detail',
                'columns': [
                    {'label': 'ФИО', 'attr': 'full_name', 'style': 'strong'},
                    {'label': 'Специализация', 'attr': 'breed.name'},
                    {'label': 'Статус', 'attr': 'is_active', 'style': 'bool_badge',
                     'true_label': 'Активен', 'true_color': 'success',
                     'false_label': 'Уволен', 'false_color': 'secondary'},
                ],
                'empty_message': 'На ринге нет экспертов.',
            },
            {
                'title': 'Расписание показов',
                'icon': 'bi-calendar-week',
                'items': ring.schedule.select_related('breed'),
                'item_url_name': 'schedule_detail',
                'columns': [
                    {'label': 'Порода', 'attr': 'breed.name', 'style': 'strong'},
                    {'label': 'Слот', 'attr': 'time_slot'},
                ],
                'empty_message': 'Расписание пусто.',
            },
        ]


# ЭКСПЕРТЫ

class ExpertListView(MessageListView):
    model = Expert
    list_title = 'Эксперты'
    list_icon = 'bi-person-workspace'
    create_url = 'expert_create'
    create_label = 'Добавить эксперта'
    empty_message = 'Пока нет ни одного эксперта.'
    update_url_name = 'expert_update'
    delete_url_name = 'expert_delete'
    detail_url_name = 'expert_detail'
    columns = [
        {'label': 'ФИО', 'attr': 'full_name', 'style': 'strong'},
        {'label': 'Специализация', 'attr': 'breed.name'},
        {'label': 'Ринг', 'attr': 'ring.number'},
        {'label': 'Клуб', 'attr': 'club.name'},
        {'label': 'Статус', 'attr': 'is_active', 'style': 'bool_badge',
         'true_label': 'Активен', 'true_color': 'success',
         'false_label': 'Уволен', 'false_color': 'secondary'},
    ]

    def get_queryset(self):
        return Expert.objects.select_related('breed', 'ring', 'club')


class ExpertCreateView(MessageCreateView):
    model = Expert
    form_class = ExpertForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('expert_list')
    cancel_url = 'expert_list'

    def get_initial(self):
        initial = super().get_initial()
        club_id = self.request.GET.get('club')
        if club_id:
            initial['club'] = club_id
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        club_id = self.request.GET.get('club')
        if club_id:
            try:
                club = Club.objects.get(pk=club_id)
                ctx['form_note'] = f'Эксперт будет принят в клуб «{club.name}».'
                ctx['cancel_url_explicit'] = reverse('club_detail', args=[club.pk])
            except Club.DoesNotExist:
                pass
        return ctx

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


class ExpertDetailView(MessageDetailView):
    model = Expert
    detail_icon = 'bi-person-workspace'
    update_url_name = 'expert_update'
    delete_url_name = 'expert_delete'
    list_url_name = 'expert_list'

    def get_detail_title(self):
        return f'Эксперт: {self.object.full_name}'

    def get_extra_actions(self):
        expert = self.object
        if expert.is_active:
            return [{
                'label': 'Уволить',
                'url': reverse('expert_fire', args=[expert.pk]),
                'icon': 'bi-person-x',
                'style': 'outline-danger',
            }]
        return [{
            'label': 'Принять обратно',
            'url': reverse('expert_rehire', args=[expert.pk]),
            'icon': 'bi-person-check',
            'style': 'outline-success',
        }]

    def get_info_rows(self):
        expert = self.object
        rows = [
            row('ФИО', expert.full_name, strong=True),
            row('Специализация', expert.breed.name,
                link=reverse('breed_detail', args=[expert.breed.pk])),
        ]
        if expert.ring:
            rows.append(row('Ринг', f'№{expert.ring.number}',
                            link=reverse('ring_detail', args=[expert.ring.pk])))
        else:
            rows.append(row('Ринг', 'Не назначен', muted=True))
        rows.append(row('Клуб', expert.club.name,
                        link=reverse('club_detail', args=[expert.club.pk])))
        rows.append(row('Статус',
                        'Активен' if expert.is_active else 'Уволен',
                        badge='success' if expert.is_active else 'secondary'))
        return rows


# МЕДАЛИ

class MedalListView(MessageListView):
    model = Medal
    list_title = 'Медали'
    list_icon = 'bi-award'
    create_url = 'medal_create'
    create_label = 'Добавить медаль'
    empty_message = 'Пока нет ни одной медали.'
    update_url_name = 'medal_update'
    delete_url_name = 'medal_delete'
    detail_url_name = 'medal_detail'
    columns = [
        {'label': 'Собака', 'attr': 'dog.name', 'style': 'strong'},
        {'label': 'Порода', 'attr': 'breed.name'},
        {'label': 'Тип', 'attr': 'get_medal_type_display', 'style': 'medal_badge'},
        {'label': 'Дата', 'attr': 'awarded_at', 'style': 'date'},
    ]

    def get_queryset(self):
        return Medal.objects.select_related('dog', 'breed')


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


class MedalDetailView(MessageDetailView):
    model = Medal
    detail_icon = 'bi-award'
    update_url_name = 'medal_update'
    delete_url_name = 'medal_delete'
    list_url_name = 'medal_list'

    def get_detail_title(self):
        return f'Медаль: {self.object.get_medal_type_display()}'

    def get_info_rows(self):
        medal = self.object
        colors = {'Золото': 'warning', 'Серебро': 'secondary', 'Бронза': 'danger'}
        return [
            row('Собака', medal.dog.name,
                link=reverse('dog_detail', args=[medal.dog.pk]), strong=True),
            row('Порода', medal.breed.name,
                link=reverse('breed_detail', args=[medal.breed.pk])),
            row('Тип', medal.get_medal_type_display(),
                badge=colors.get(medal.get_medal_type_display(), 'secondary')),
            row('Дата награждения', medal.awarded_at.strftime('%d.%m.%Y')),
        ]


# РАСПИСАНИЯ

class ScheduleListView(MessageListView):
    model = RingBreedSchedule
    list_title = 'Расписания рингов'
    list_icon = 'bi-calendar-week'
    create_url = 'schedule_create'
    create_label = 'Добавить слот'
    empty_message = 'Пока нет ни одного слота расписания.'
    update_url_name = 'schedule_update'
    delete_url_name = 'schedule_delete'
    detail_url_name = 'schedule_detail'
    columns = [
        {'label': 'Ринг', 'attr': 'ring.number'},
        {'label': 'Порода', 'attr': 'breed.name', 'style': 'strong'},
        {'label': 'Слот', 'attr': 'time_slot'},
    ]

    def get_queryset(self):
        return RingBreedSchedule.objects.select_related('ring', 'breed')


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
        return f'Слот обновлён.'


class ScheduleDeleteView(MessageDeleteView):
    model = RingBreedSchedule
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')
    cancel_url = 'schedule_list'

    def get_success_message(self, obj):
        return f'Слот удалён.'


class ScheduleDetailView(MessageDetailView):
    model = RingBreedSchedule
    detail_icon = 'bi-calendar-week'
    update_url_name = 'schedule_update'
    delete_url_name = 'schedule_delete'
    list_url_name = 'schedule_list'

    def get_detail_title(self):
        return f'Расписание: {self.object}'

    def get_info_rows(self):
        s = self.object
        return [
            row('Ринг', f'№{s.ring.number}',
                link=reverse('ring_detail', args=[s.ring.pk]), strong=True),
            row('Порода', s.breed.name,
                link=reverse('breed_detail', args=[s.breed.pk])),
            row('Слот', s.time_slot),
        ]

# ОТЧЁТЫ

@login_required
def medals_by_club(request):
    clubs = Club.objects.all()
    rows = []

    for club in clubs:
        medals = Medal.objects.filter(dog__club=club).values('medal_type')
        counts = defaultdict(int)
        for m in medals:
            counts[m['medal_type']] += 1

        rows.append({
            'club': club,
            'gold': counts.get('gold', 0),
            'silver': counts.get('silver', 0),
            'bronze': counts.get('bronze', 0),
            'total': sum(counts.values()),
        })

    rows.sort(key=lambda r: r['total'], reverse=True)

    return render(request, 'medals/by_club.html', {'rows': rows})


@login_required
def record_holders(request):
    dogs = (
        Dog.objects
        .annotate(medal_count=Count('medals'))
        .filter(medal_count__gt=0)
        .select_related('breed', 'owner', 'club')
    )

    by_breed = defaultdict(list)
    for dog in dogs:
        by_breed[dog.breed].append(dog)

    records = []
    for breed, breed_dogs in by_breed.items():
        max_count = max(d.medal_count for d in breed_dogs)
        champions = [d for d in breed_dogs if d.medal_count == max_count]
        total_breed_medals = sum(d.medal_count for d in breed_dogs)
        records.append({
            'breed': breed,
            'max_count': max_count,
            'champions': champions,
            'total_breed_medals': total_breed_medals,
        })

    records.sort(key=lambda x: (-x['max_count'], x['breed'].name))

    return render(request, 'medals/record_holders.html', {'records': records})


# ДЕЙСТВИЯ ПРЕДСЕДАТЕЛЯ КЛУБА И ОРГАНИЗАТОРА

class ConfirmActionView(LoginRequiredMixin, View):
    model = None
    action_title = ''
    action_warning = ''
    redirect_to = ''

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        return render(request, 'core/confirm_action.html', {
            'object': obj,
            'action_title': self.action_title,
            'action_warning': self.action_warning,
            'cancel_url': reverse(self.redirect_to, args=[pk]),
        })

    def post(self, request, pk):
        obj = self.get_object(pk)
        self.perform_action(obj)
        messages.success(request, self.get_success_message(obj))
        return redirect(self.redirect_to, pk=pk)

    def perform_action(self, obj):
        raise NotImplementedError

    def get_success_message(self, obj):
        return 'Действие выполнено.'


class DogDisqualifyView(ConfirmActionView):
    model = Dog
    action_title = 'Отстранить собаку от участия'
    action_warning = 'Собака не сможет участвовать в выставке до восстановления.'
    redirect_to = 'dog_detail'

    def perform_action(self, obj):
        obj.is_disqualified = True
        obj.save(update_fields=['is_disqualified'])

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» отстранена от участия.'


class DogRestoreView(ConfirmActionView):
    model = Dog
    action_title = 'Восстановить собаку в участии'
    redirect_to = 'dog_detail'

    def perform_action(self, obj):
        obj.is_disqualified = False
        obj.save(update_fields=['is_disqualified'])

    def get_success_message(self, obj):
        return f'Собака «{obj.name}» снова участвует.'


class ExpertFireView(ConfirmActionView):
    model = Expert
    action_title = 'Уволить эксперта из клуба'
    action_warning = 'Эксперт потеряет активный статус и не сможет судить.'
    redirect_to = 'expert_detail'

    def perform_action(self, obj):
        obj.is_active = False
        obj.save(update_fields=['is_active'])

    def get_success_message(self, obj):
        return f'Эксперт «{obj.full_name}» уволен.'


class ExpertRehireView(ConfirmActionView):
    model = Expert
    action_title = 'Принять эксперта обратно в клуб'
    redirect_to = 'expert_detail'

    def perform_action(self, obj):
        obj.is_active = True
        obj.save(update_fields=['is_active'])

    def get_success_message(self, obj):
        return f'Эксперт «{obj.full_name}» снова активен.'
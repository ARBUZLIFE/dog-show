from django.db import models


class Club(models.Model):
    name = models.CharField('Название', max_length=150, unique=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField('Название породы', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Owner(models.Model):
    full_name = models.CharField('ФИО', max_length=200)
    passport_data = models.CharField('Паспортные данные', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Хозяин'
        verbose_name_plural = 'Хозяева'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Ring(models.Model):
    number = models.PositiveIntegerField('Номер ринга')
    address = models.CharField('Адрес', max_length=255)
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='rings',
        verbose_name='Клуб',
    )

    class Meta:
        verbose_name = 'Ринг'
        verbose_name_plural = 'Ринги'
        unique_together = [('club', 'number')]
        ordering = ['club', 'number']

    def __str__(self):
        return f'Ринг №{self.number} ({self.club.name})'


class Expert(models.Model):
    full_name = models.CharField('ФИО', max_length=200)
    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        related_name='experts',
        verbose_name='Специализация (порода)',
    )
    ring = models.ForeignKey(
        Ring,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='experts',
        verbose_name='Ринг',
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='experts',
        verbose_name='Клуб',
    )
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Dog(models.Model):
    name = models.CharField('Кличка', max_length=100)
    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        related_name='dogs',
        verbose_name='Порода',
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='dogs',
        verbose_name='Клуб',
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name='dogs',
        verbose_name='Хозяин',
    )
    age = models.PositiveIntegerField('Возраст (лет)')
    pedigree_number = models.CharField('Номер родословной', max_length=50, unique=True)
    parent_names = models.CharField('Клички родителей', max_length=255)
    last_vaccination_date = models.DateField('Дата последней прививки')
    is_disqualified = models.BooleanField('Отстранена', default=False)

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.breed.name})'


class Medal(models.Model):
    MEDAL_TYPES = [
        ('gold', 'Золото'),
        ('silver', 'Серебро'),
        ('bronze', 'Бронза'),
    ]

    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name='medals',
        verbose_name='Собака',
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        related_name='medals',
        verbose_name='Порода',
    )
    medal_type = models.CharField('Тип медали', max_length=10, choices=MEDAL_TYPES)
    awarded_at = models.DateField('Дата награждения')

    class Meta:
        verbose_name = 'Медаль'
        verbose_name_plural = 'Медали'
        ordering = ['-awarded_at']

    def __str__(self):
        return f'{self.get_medal_type_display()} — {self.dog.name}'


class RingBreedSchedule(models.Model):
    ring = models.ForeignKey(
        Ring,
        on_delete=models.CASCADE,
        related_name='schedule',
        verbose_name='Ринг',
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name='schedule',
        verbose_name='Порода',
    )
    time_slot = models.CharField('Временной слот', max_length=50)

    class Meta:
        verbose_name = 'Расписание ринга'
        verbose_name_plural = 'Расписания рингов'
        unique_together = [('ring', 'breed', 'time_slot')]
        ordering = ['ring', 'time_slot']

    def __str__(self):
        return f'{self.ring} — {self.breed.name} ({self.time_slot})'
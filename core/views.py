from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Dog
from .forms import DogForm


def home(request):
    return render(request, 'home.html')


@login_required
def dog_list(request):
    dogs = Dog.objects.select_related('breed', 'club', 'owner').all()
    return render(request, 'core/dog_list.html', {'dogs': dogs})


@login_required
def dog_create(request):
    if request.method == 'POST':
        form = DogForm(request.POST)
        if form.is_valid():
            dog = form.save()
            messages.success(request, f'Собака «{dog.name}» успешно добавлена.')
            return redirect('dog_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = DogForm()
    return render(request, 'core/dog_form.html', {
        'form': form,
        'title': 'Добавить собаку',
        'button_label': 'Создать',
    })


@login_required
def dog_update(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, f'Собака «{dog.name}» обновлена.')
            return redirect('dog_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = DogForm(instance=dog)
    return render(request, 'core/dog_form.html', {
        'form': form,
        'title': f'Редактировать: {dog.name}',
        'button_label': 'Сохранить',
    })


@login_required
def dog_delete(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        name = dog.name
        dog.delete()
        messages.success(request, f'Собака «{name}» удалена.')
        return redirect('dog_list')
    return render(request, 'core/dog_confirm_delete.html', {'dog': dog})
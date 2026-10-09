from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


ORGANIZER_GROUP = 'Организатор выставки'
CHAIRMAN_GROUP = 'Председатель клуба'


class BaseGroupRequiredMixin(LoginRequiredMixin):
    required_groups = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.groups.filter(name__in=self.required_groups).exists():
            raise PermissionDenied('У вас нет прав для этого действия.')
        return super().dispatch(request, *args, **kwargs)


class OrganizerRequiredMixin(BaseGroupRequiredMixin):
    required_groups = (ORGANIZER_GROUP,)


class ChairmanRequiredMixin(BaseGroupRequiredMixin):
    required_groups = (CHAIRMAN_GROUP,)


class StaffRequiredMixin(BaseGroupRequiredMixin):
    required_groups = (ORGANIZER_GROUP, CHAIRMAN_GROUP)


def user_is_organizer(user):
    return user.is_superuser or user.groups.filter(name=ORGANIZER_GROUP).exists()


def user_is_chairman(user):
    return user.is_superuser or user.groups.filter(name=CHAIRMAN_GROUP).exists()


def user_is_staff(user):
    return user_is_organizer(user) or user_is_chairman(user)
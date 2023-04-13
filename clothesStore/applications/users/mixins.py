# import models
from .models import User

# import django packages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

def check_role(role, user_role):

    if(role == '0' or role == user_role):
        return True
    else:
        return False

class AdminPermissionMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:login')

    def dispatch(self, request, *args , **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_role(request.user.ocupation, '0'):
            return HttpResponseRedirect(
                reverse(
                    'home_app:home'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class WorkerPermissionMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_role(request.user.ocupation, '1'):
            return HttpResponseRedirect(
                reverse(
                    'home_app:home'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class ClientPermissionMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_role(request.user.ocupation, '2'):
            return HttpResponseRedirect(
                reverse(
                    'home_app:home'
                )
            )
        return super().dispatch(request, *args, **kwargs)
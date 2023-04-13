from django.shortcuts import render
from django.views.generic import FormView, View, ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
# required forms
from .forms import UserRegisterForm

# required models
from .models import User

# extra functions
from .functions import code_generator

# json information function
from django.conf import settings

# send emails package
from django.core.mail import send_mail

# import forms
from .forms import VerificationForm, LoginForm, UpdatePasswordForm

# package to authenticate users
from django.contrib.auth import authenticate, login, logout

# Permissions
from .mixins import AdminPermissionMixin


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'auth/register.html'

    def form_valid(self, form):

        # generate token
        code = code_generator()

        # if everything is ok, create user
        user = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            # Extra fields
            full_name=form.cleaned_data['full_name'],
            gender=form.cleaned_data['gender'],
            code_register=code,
        )
        # send code to confirm account
        subject = "Account confirmation"
        message = "Verification code: " + code
        sender = settings.EMAIL_SENDER

        # send email
        send_mail(subject, message, sender, [form.cleaned_data['email'],])

        # redirect the user to insert the code and verify the account

        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': user.id}
            )
        )

class CodeVerificationView(FormView):
    template_name = 'auth/account_verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs
    
    def form_valid(self, form):

        # If everything is correct, the status of the user is updated
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)

class LoginUserView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        # Create a session for the user
        login(self.request, user)

        return super(LoginUserView, self).form_valid(form)

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'home_app:home'
            )
        )

class UpdatePassword(FormView):
    template_name = 'auth/recover_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')

    """ For this view the user must be authenticated """

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['old_password']
        )

        if user:
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
        login(self.request, user)

        return super(UpdatePassword, self).form_valid(form)

class ListUsersView(AdminPermissionMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/users.html'
    paginate_by = 5

class DetailsUserView(DetailView):
    template_name = 'users/detail_user.html'
    context_object_name = 'user'
    
    def get_queryset(self):
        user = User.objects.filter(
            id=self.kwargs['pk']
        )
        return user

class BlockUserView(View):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(
            id=self.kwargs['pk']
        )
        user.is_active = False
        user.save()

        return HttpResponseRedirect(
            reverse(
                'users_app:users'
            )
        )

class AllowUser(View):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(
            id=self.kwargs['pk']
        )
        user.is_active = True
        user.save()

        return HttpResponseRedirect(
            reverse(
                'users_app:users'
            )
        )


    








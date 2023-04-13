from django import forms
# Required model
from .models import User

# authenticate user package
from django.contrib.auth import authenticate

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-field register-field'
            }
        )
    )

    password2 = forms.CharField(
        label='Repeat password',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat password',
                'class': 'form-field register-field'
            }
        )
    )


    class Meta:
        model = User
        fields = (
            'email',
            'full_name',
            'password1',
            'password2',
            'gender'
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'email@email.com',
                    'class': 'form-field register-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Jhon Doe',
                    'class': 'form-field register-field',
                }
            ),
            'gender':forms.Select(
                choices=User.GENDER_CHOICES,
                attrs={
                    'class':'form-field register-field'
                }
            ),
            
        }
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Passwords are different')

class VerificationForm(forms.Form):
    
    code_register = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'XXXXXX',
                'class': 'form-field login-field'
            }
        )
    )

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    
    def clean_code_register(self):
        code = self.cleaned_data['code_register']

        if(len(code) == 6):
            # verify if the user exists 
            user = User.objects.code_validation(
                self.id_user,
                code
            )
            if not user:
                raise forms.ValidationError('Invalid code')
            else:
                User.objects.filter(id=self.id_user).update(
                    code_register = None
                )
        else: 
            raise forms.ValidationError('Invalid code')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username',
                'class': 'form-field login-field'
            }
        )
    )

    password = forms.CharField(
        label='password',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password',
                'class': 'form-field login-field'
            }
        )
    )

    # vlidate information
    def clean(self):

        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Wrong credentials')
        
        return self.cleaned_data

class UpdatePasswordForm(forms.Form):

    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username',
                'class': 'form-field login-field'
            }
        )
    )

    old_password = forms.CharField(
        label='Old password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'old password',
                'class': 'form-field login-field'
            }
        )
    )

    new_password = forms.CharField(
        label='New password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'New password',
                'class': 'form-field login-field'
            }
        )
    )




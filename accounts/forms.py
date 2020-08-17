from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class UserRegisterForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'نام کاربری بیشتر از ۴ کاراکتر می‌باشد'}),
            label='نام کاربری',
            min_length=4,
            max_length=25,
    )
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی معتبر وارد کنید'}),
            label='پست الکترونیکی'
    )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور قوی و بیشتر از ۷ کاراکتر انتخاب کنید'}),
            label='رمز عبور',
            min_length=7,
    )


class UserLoginForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'نام کاربری خود را وارد کنید'}),
            label='نام کاربری'
    )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور خود را وارد کنید'}),
            label='رمز عبور',
            min_length=8
    )



class UserForgetForm(forms.Form):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی خود را وارد کنید'}),
            label='پست الکترونیکی')


class ResendActiveForm(forms.Form):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی خود را وارد کنید'}),
            label='پست الکترونیکی')


class UserChangePasswordForm(forms.Form):
    password1 = forms.CharField(
            label='رمز عبور جدید',
            min_length=7,
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور قوی و بیشتر از ۷ کاراکتر'}))

    password2 = forms.CharField(
            label='تایید رمز عبور',
            min_length=7,
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور خود را تایید کنید'}))

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('رمز عبور تایید نمی‌شود')

        return pass2



class ProfileForm(forms.Form):
    phone = forms.CharField(min_length=11, max_length=11,
                            label='شماره موبایل',
                            required=True,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'مثال: ۰۹۱۲۱۱۱۲۲۳۳'
                            }))
    first_name = forms.CharField(label='نام',
                                 widget=forms.TextInput({
                                     'placeholder': 'نام خود را وارد کنید'
                                 }),
                                 max_length=25,
                                 min_length=2,
                                 required=True)
    last_name = forms.CharField(label='نام خانوادگی',
                                widget=forms.TextInput({
                                    'placeholder': 'نام خانوادگی خود را وارد کنید'
                                }),
                                max_length=25,
                                min_length=2,
                                required=True)
    avatar = forms.ImageField(label='تصویر پروفایل',
                              required=False)
    province = forms.CharField(label='استان',
                           required=True,
                           max_length=100,
                           min_length=2,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'نام استان'
                           }))
    city = forms.CharField(label='شهر',
                           required=True,
                           max_length=100,
                           min_length=2,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'نام شهر'
                           }))
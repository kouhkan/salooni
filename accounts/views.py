from random import randint

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import (UserRegisterForm,
                    UserLoginForm,
                    UserForgetForm,
                    ResendActiveForm,
                    UserChangePasswordForm,
                    ProfileForm)
from .tasks import (user_register_task,
                    user_resend_code_task,
                    user_change_password_task,
                    user_verify_task,
                    user_login_task,
                    user_forget_task,
                    signer)
from payments.models import Payment
from reservation.models import Reservation


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = user_register_task.delay(cd['username'], cd['email'], cd['password'])
            if user.get() == 1:
                request.session['user_email'] = cd['email']
                messages.success(request, 'ثبت نام', 'success')
                return redirect('accounts:user_active')
            elif user.get() == 2:
                messages.error(request, 'کاربری با این پست الکترونیکی وجود دارد', 'danger')
                return redirect('accounts:user_register')
            else:
                pass
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/user_register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            check_login = user_login_task.delay(cd['username'])

            if check_login.get() == 2:
                messages.error(request, 'کاربر فعال نیست', 'danger')
                return redirect('accounts:user_active')
            elif check_login.get() == 3:
                messages.error(request, 'کاربر وجود ندارد', 'danger')
                return redirect('accounts:user_register')
            else:
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'وارد شدید', 'success')
                    return redirect('accounts:user_index')
                else:
                    messages.error(request, 'نام کاربری یا رمز عبور صحیح نیست', 'danger')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/user_login.html', context)


def user_active(request):
    return render(request, 'accounts/user_active.html')


def user_change_password(request, email=None, code=None):
    if email is not None and code is not None:
        if request.method == 'POST':
            form = UserChangePasswordForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                result = user_change_password_task.delay(email, code, cd['password1'], cd['password2'])

                if result.get() == 1:
                    messages.success(request, 'رمز عوض شد', 'success')
                    return redirect('accounts:user_login')
                elif result.get() == 2:
                    messages.success(request, 'رمز عوض نشد', 'danger')
                    return redirect('accounts:user_forget')
                elif result.get() == 3:
                    messages.success(request, 'لینک معتبر نیست', 'danger')
                    return redirect('accounts:user_forget')
                else:
                    pass
        else:
            form = UserChangePasswordForm()

        context = {
            'form': form
        }
        return render(request, 'accounts/user_change_pssword.html', context)
    else:
        return render(request, 'accounts/send_link.html')


def user_forget(request):
    if request.method == 'POST':
        form = UserForgetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            get_user = get_object_or_404(User, email=user_email)
            if get_user.is_active:
                active_code = randint(1000, 9999)
                result = user_forget_task.delay(user_email, active_code)
                if result.get() == 1:
                    messages.success(request, 'لینک تغییر رمز عبور ارسال شد', 'success')
                    return redirect('accounts:user_change_password_reset')
                else:
                    messages.error(request, 'خطایی رخ داده است', 'danger')
                    return redirect('accounts:user_forget')
            else:
                user_resend_code_task.delay(user_email)
                messages.error(request, 'حساب شما فعال نیست', 'danger')
                return redirect('accounts:resend_code')
    else:
        form = UserForgetForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/user_forget.html', context)


def resend_code(request):
    if request.method == 'POST':
        form = ResendActiveForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            result = user_resend_code_task.delay(email)
            if result.get() == 1:
                messages.success(request, 'لینک فعال‌سازی برای شما ارسال شد', 'success')
                return redirect('accounts:user_active')
            elif result.get() == 4:
                messages.error(request, 'حساب کاربری وجودندارد', 'danger')
                return redirect('accounts:user_register')
            else:
                return redirect('accounts:user_register')
    else:
        form = ResendActiveForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/user_resne_active_mail.html', context)




def user_logout(request):
    logout(request)
    messages.success(request, 'خروج', 'success')
    return redirect('accounts:user_login')


def user_verify(request, email, code):
    user_email = signer.unsign(email)
    result = user_verify_task.delay(user_email, code)

    if result.get() == 1:
        messages.success(request, 'فعال شد', 'success')
        return redirect('accounts:user_login')
    elif result.get() == 2:
        messages.error(request, 'کد نادرست است', 'danger')
        return redirect('accounts:user_register')
    elif result.get() == 3:
        messages.error(request, 'کد  منقضی شده است', 'danger')
        return redirect('accounts:resend_code')


@login_required
def user_index(request):
    reserves = Reservation.objects.filter(user=request.user, status='r')
    payments = Payment.objects.filter(reserve__user=request.user)
    get_user = User.objects.get(username=request.user.username)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            get_user.first_name = cd['first_name']
            get_user.last_name = cd['last_name']
            get_user.phone = cd['phone']
            get_user.user_profile.avatar = cd['avatar']
            get_user.user_profile.province = cd['province']
            get_user.user_profile.city = cd['city']
            get_user.save()
            messages.success(request, 'پروفایل شما با موفقیت ویرایش شد', 'success')
            return redirect('accounts:user_index')
    else:
        form = ProfileForm(initial={'first_name': get_user.first_name,
                                'last_name': get_user.last_name,
                                'phone': get_user.phone,
                                'avatar': get_user.user_profile.avatar,
                                'province': get_user.user_profile.province,
                                'city': get_user.user_profile.city})
    context = {
        'form': form,
        'reserves': reserves,
        'payments': payments

    }
    return render(request, 'accounts/index.html', context)


@login_required
def user_manager(request):
    if request.user.is_staff:
        get_reservations = Reservation.objects.filter(saloon__owner=request.user, status='r')
        return render(request, 'accounts/manager/index.html', {'reserves': get_reservations})
    else:
        return redirect('accounts:user_login')
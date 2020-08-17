from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Saloon, Image
from reservation.models import Reservation
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ReserveDatetime, SelectTypeForm, SelectGenderForm, SearchSaloonForm
from django.contrib import messages
from khayyam import *
from datetime import datetime, date
from suds import Client
from payments.models import Payment
from django.core.cache import cache
from django.views.decorators.cache import cache_page


@cache_page(60 * 20)
def saloon_list(request):
	cache_time = 60 * 20
	cache_key = 'cache_key2'
	saloons_list = cache.get(cache_key)
	if not saloons_list:
		saloons_list = Saloon.active_saloons.all()

	cache.set(cache_key, saloons_list, cache_time)
	type_form = SelectTypeForm()
	gender_form = SelectGenderForm()
	search_form = SearchSaloonForm()

	if request.method == 'GET':
		type = request.GET.get('type')
		gender = request.GET.get('gender')

		if type is not None and gender is not None:
			saloons_list = Saloon.active_saloons.filter(type=type,
			                                            gender=gender)

	if request.method == 'GET':
		search_text = request.GET.get('search_text')
		if search_text is not None and search_text != u"":
			search_text = request.GET.get('search_text')
			saloons_list = Saloon.active_saloons.filter(city__contains=search_text)


	context = {
		'saloons_list': saloons_list,
		'type_form':  type_form,
		'gender_form':  gender_form,
		'search_form': search_form
	}
	return render(request, 'saloons/saloons_list.html', context)


# def search_city(request):
#
#
# 		return render(request, 'saloons/saloons_list.html', {'saloons_list': city})

@cache_page(60 * 20)
def saloon_detail(request, slug):
	cache_key = f'saloon-{slug}'
	images_cache_key = f'images-{cache_key}'
	get_saloon = cache.get(cache_key)
	images = cache.get(images_cache_key)
	if not get_saloon or not images:
		get_saloon = get_object_or_404(Saloon, slug=slug)
		images = Image.objects.filter(saloon=get_saloon)

	cache.set(cache_key, get_saloon, 60 * 20)
	cache.set(images_cache_key, images, 60 * 20)

	if request.method == 'POST':
		if request.user.is_authenticated:
			form = ReserveDatetime(request.POST)
			if form.is_valid():
				reserved_date = form.cleaned_data['datetime']
				hour = form.cleaned_data['hour']
				make_str = f'{reserved_date}'
				# Save to database
				make_datetime = datetime.strptime(make_str, '%Y-%m-%d')
				# print('$'*51, make_datetime)
				# Show to user
				make_jalali = JalaliDate(make_datetime).strftime('%Y-%m-%d')
				# print('='*51, make_jalali)
				if make_datetime < datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'):
					messages.error(request, 'تاریخ انتخاب شده شما گذشته است', 'warning')
					return redirect('saloons:saloons_detail', slug)
				if hour not in range(get_saloon.start_time, get_saloon.end_time):
					messages.error(request, 'سانس انتخاب شده شما خارج از محدوده فعالیت {} می‌باشد!'
					               .format(get_saloon.name), 'warning')
					return redirect('saloons:saloons_detail', slug)
				create_reserve = Reservation.objects.filter(reserve_date__exact=make_datetime,
				                                            saloon=get_saloon,
				                                            hour=hour,
				                                            status='r').exists()
				if create_reserve:
					messages.error(request, 'سانس مد نظر شما رزرو شده است، ساعت و'
					                        ' یا تاریخ دیگری را انتخاب نمایید', 'warning')
				else:
					reserve = Reservation.objects.create(user=request.user,
					                                     saloon=get_saloon,
					                                     reserve_date=make_datetime,
					                                     hour=hour)
					reserve.save()
					messages.success(request, 'با موفقیت سانس خود را موقتا انتخاب کردید.', 'success')
					return redirect('saloons:payment', reserve.id, get_saloon.amount)
			else:
				print('not valid')
		else:
			messages.success(request, 'برای ثبت رزرو لطفا وارد حساب خود شوید', 'warning')
			return redirect('accounts:user_login')
	else:
		form = ReserveDatetime()
	context = {
		'saloon': get_saloon,
		'images': images,
		'form': form
	}
	return render(request, 'saloons/saloon_detail.html', context)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات پرداخت"
mobile = '09123456789'
amount = None
CallbackURL = 'http://localhost:8000/payment/verify/'


@login_required
def payment(request, reserve_id, amount):
	request.session[f'{request.user}'] = {
		'user': {
			'reserve_id': reserve_id,
			'amount': amount + 1000
		},
	}
	result = client.service.PaymentRequest(
			MERCHANT, amount + 1000, description, request.user.email, mobile, CallbackURL)
	if result.Status == 100:
		return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
	else:
		return HttpResponse('Error code: ' + str(result.Status))


@login_required
def verify(request):
	if request.GET.get('Status') == 'OK':
		result = client.service.PaymentVerification(
				MERCHANT, request.GET['Authority'], request.session[f'{request.user}'].get('user')['amount'])
		if result.Status == 100:
			try:
				reserve_id = request.session[f'{request.user}'].get('user')['reserve_id']
				reserve = Reservation.objects.get(id=reserve_id)
				reserve.status = 'r'
				reserve.save()
				Payment.objects.create(reserve=reserve,
				                       authority=request.GET['Authority'],
				                       refid=0,
				                       status=result.Status,
				                       paid=True)
				messages.success(request, 'رزرو سالن با موفقیت انجام شد', 'success')
				del request.session[f'{request.user}']
				return redirect('accounts:user_index')
			except Reservation.DoesNotExist:
				messages.success(request, 'رزرو نامعتبر', 'danger')
				return redirect('saloons:saloons_list')


		elif result.Status == 101:
			return HttpResponse('Transaction submitted')
		else:
			return HttpResponse('Transaction failed')
	else:
		try:
			reserve_id = request.session[f'{request.user}'].get('user')['reserve_id']
			reserve = Reservation.objects.get(id=reserve_id)
			Payment.objects.create(reserve=reserve,
			                       authority=request.GET['Authority'],
			                       refid=0,
			                       status=200,
			                       paid=False)
			del request.session[f'{request.user}']
			messages.success(request, 'عملیات پرداخت کنسل شد', 'danger')
			return redirect('saloons:saloons_list')
		except Reservation.DoesNotExist:
			messages.success(request, 'رزرو نامعتبر', 'danger')
			return redirect('saloons:saloons_list')



def saloon_city(request, slug):
	saloons = get_list_or_404(Saloon, city=slug)

	context = {
		'saloons_list': saloons
	}
	return render(request, 'saloons/saloon_filter.html', context)


def saloon_province(request, slug):
	saloons = get_list_or_404(Saloon, province=slug)

	context = {
		'saloons_list': saloons
	}
	return render(request, 'saloons/saloon_filter.html', context)
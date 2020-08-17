from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from django.contrib import messages


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = cd['first_name'] + cd['last_name']
			Contact.objects.create(user=user,
			                       email=cd['email'],
			                       subject=cd['subject'],
			                       body=cd['body'])
			messages.success(request, 'پیام شما برای ما ارسال شد', 'success')
			return redirect('saloons:saloons_list')
	else:
		form = ContactForm()

	return render(request, 'contacts/contact.html', {'form': form})


def about(request):
	return render(request, 'contacts/about.html')
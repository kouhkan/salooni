from django import forms


class ContactForm(forms.Form):
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
	                             required=False)
	subject = forms.CharField(label='موضوع',
	                          max_length=70,
	                          min_length=10,
	                          widget=forms.TextInput({
		                          'placeholder': 'موضوع پیام را با حداکثر ۷۰ کاراکتر بنویسید'
	                          }))
	body = forms.CharField(label='متن پیام',
	                          max_length=1000,
	                          min_length=10,
	                          widget=forms.Textarea({
		                          'placeholder': 'حداکثر ۱۰۰۰ کاراکتر'
	                          }))
	email = forms.EmailField(label='پست الکترونیکی',
	                         widget=forms.EmailInput(attrs={
		                         'placeholder': 'پست الکترونیکی خود را برای دریافت پاسخ وارد کنید'
	                         }),
	                         max_length=100)
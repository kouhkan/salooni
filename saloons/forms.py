from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class ReserveDatetime(forms.Form):
	datetime = JalaliDateField(label='انتخاب تاریخ',
	                           widget=AdminJalaliDateWidget)
	hour = forms.IntegerField(max_value=24, min_value=1,
	                            label='انتخاب ساعت')



class SelectTypeForm(forms.Form):
	TYPE = (
		('su', 'چمن'),
		('sa', 'سالن'),
	)
	type = forms.ChoiceField(choices=TYPE,
	                         label='انتخاب نوع')


class SelectGenderForm(forms.Form):
	GENDER = (
		('b', 'بانوان و آقایان'),
		('m', 'آقایان'),
		('f', 'بانوان'),
	)
	gender = forms.ChoiceField(choices=GENDER,
	                           label='انتخاب جنسیت')


class SearchSaloonForm(forms.Form):
	search_text = forms.CharField(label='جستجو شهر',
	                         widget=forms.TextInput({
		                         'placeholder': 'نام شهر خود را بنویسید ...',
                                 'id': 'search_city'}))
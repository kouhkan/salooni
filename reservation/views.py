from django.shortcuts import render
from .models import Reservation
from accounts.models import User
from saloons.models import Saloon
from django.contrib.auth.decorators import login_required


@login_required
def create_reserve(request, saloon_id):
	return None
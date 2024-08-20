from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
from django.contrib.auth.decorators import login_required
from .forms import Enable2FAForm
from django.contrib.auth.views import LoginView
from .models import CustomUser
from django.contrib.auth import logout
from django.contrib import messages

def generate_totp_key():
    return random_hex(20)

def signup(request):
    if request.user.is_authenticated:
        return redirect('success_page')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            enable_2fa = form.cleaned_data.get('enable_2fa')
            user.enable_2fa = enable_2fa
            if enable_2fa:
                totp_key = generate_totp_key()
                request.session['enable_2fa'] = True
                user.save()
                device = TOTPDevice.objects.create(user=user, key=totp_key)
                device.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('enable_2fa')
            else:
                request.session['enable_2fa'] = False
                user.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('success_page')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('success_page')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.enable_2fa:
                    request.session['pre_2fa_user_id'] = user.id
                    request.session['pre_2fa_password'] = password
                    return redirect('verify_2fa')
                else:
                    login(request, user)
                    return redirect('success_page')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def enable_2fa(request):
    if request.method == 'POST':
        form = Enable2FAForm(request.user, request.POST)
        if form.is_valid():
            return redirect('success_page')
    else:
        form = Enable2FAForm(request.user)

    try:
        totp_device, created = TOTPDevice.objects.get_or_create(user=request.user)
        if created:
            totp_device.save()
        qr_code_url = totp_device.config_url
    except Exception as e:
        qr_code_url = None

    return render(request, 'enable_2fa.html', {'form': form, 'qr_code_url': qr_code_url, 'error': str(e) if qr_code_url is None else None})


def verify_2fa(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        user_id = request.session.get('pre_2fa_user_id')
        if not user_id:
            return redirect('login')
        
        user = CustomUser.objects.get(id=user_id)
        device = TOTPDevice.objects.filter(user=user).first()

        if device and device.verify_token(code):
            login(request, user)
            request.session.pop('pre_2fa_user_id', None)
            request.session.pop('pre_2fa_password', None)
            return redirect('success_page')
        else:
            return render(request, 'verify_2fa.html', {'error': 'Invalid 2FA code.'})

    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)
    devices = TOTPDevice.objects.filter(user=user)
    return render(request, 'verify_2fa.html', {'devices': devices})

@login_required
def success_page(request):
    return render(request, 'success_page.html')

def custom_csrf_failure_view(request, reason=""):
    return render(request, 'crsf_error.html', {'reason': reason})

import logging
import json
import requests
import smtplib
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from django.views.decorators.csrf import csrf_exempt
from .utils import register_user  # Removed `authenticate_user` since Django handles authentication

logger = logging.getLogger('django.security')

LOGIC_APP_URL = ""

# ✅ Helper Function to Get Client IP
def get_client_ip(request):
    """ Get client IP address from request headers """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# ✅ Azure Logic App Integration: Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            ip = get_client_ip(request)
            logger.info(f'User {username} logged in successfully from {ip}.')

            # ✅ Send Login Success Data to Logic App
            try:
                payload = {
                    "username": username,
                    "login_status": "Success",
                    "ip_address": ip
                }
                requests.post(LOGIC_APP_URL, json=payload)
            except Exception as e:
                logger.error(f"Error sending login data to Logic App: {e}")

            return redirect('home')  # Redirect to home page

        else:
            logger.warning(f'Failed login attempt for username: {username}')
            
            # ✅ Send Failed Login Attempt Data to Logic App
            try:
                payload = {
                    "username": username,
                    "login_status": "Failed",
                    "ip_address": get_client_ip(request)
                }
                requests.post(LOGIC_APP_URL, json=payload)
            except Exception as e:
                logger.error(f"Error sending failed login data to Logic App: {e}")

    return render(request, 'accounts/login.html')


# ✅ Log Successful Login
@receiver(user_logged_in)
def send_login_alert(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    data = {
        "username": user.username,
        "email": user.email,
        "login_time": str(user.last_login),
        "ip_address": ip
    }

    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(LOGIC_APP_URL, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Raise error if request fails
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending data to Logic App: {e}")


# ✅ Log Failed Login and Send Email Alert
@receiver(user_login_failed)
def failed_login_alert(sender, credentials, request, **kwargs):
    username = credentials.get('username', 'Unknown')
    ip = get_client_ip(request)

    try:
        user = User.objects.get(username=username)
        recipient_email = user.email  # Get registered email
    except User.DoesNotExist:
        recipient_email = None  # User not found

    if recipient_email:
        # Create email alert payload
        alert_data = {
            "email": recipient_email,
            "subject": "🔴 Security Alert: Failed Login Attempt",
            "message": f"A failed login attempt was detected for your account from IP: {ip}. If this wasn't you, please reset your password."
        }

        # Send request to Azure Logic App
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(LOGIC_APP_URL, json=alert_data, headers=headers)
            response.raise_for_status()
            logger.info(f"🚀 Alert sent successfully to {recipient_email}")
        except requests.exceptions.RequestException as e:
            logger.error(f"⚠️ Failed to send alert: {e}")


# ✅ Log User Logout
@login_required
def logout_view(request):
    username = request.user.username
    ip = get_client_ip(request)
    logout(request)
    logger.info(f'User {username} logged out successfully from {ip}.')
    return redirect('login')  # Redirect to login page


# ✅ Detect Suspicious Activity (Multiple Failed Attempts)
@receiver(user_login_failed)
def track_failed_attempts(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    username = credentials.get('username', 'unknown user')

    failed_attempts = cache.get(ip, 0) + 1
    cache.set(ip, failed_attempts, timeout=300)  # Store failed attempts for 5 minutes
    
    if failed_attempts > 3:  # More than 3 failed attempts
        logger.error(f"🚨 Suspicious activity detected: Multiple failed logins from {ip}.")

        # ✅ Notify Logic App of Suspicious Activity
        try:
            payload = {
                "username": username,
                "login_status": "Suspicious",
                "ip_address": ip,
                "failed_attempts": failed_attempts
            }
            requests.post(LOGIC_APP_URL, json=payload)
        except Exception as e:
            logger.error(f"Error sending suspicious activity data to Logic App: {e}")


# ✅ Home Page View
def home_view(request):
    return render(request, 'accounts/home.html')


# ✅ Send Email Function (Using Logic App)
def send_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request body
            recipient = data.get("email")
            subject = data.get("subject", "No Subject")
            message = data.get("message", "No Message")

            if not recipient:
                return JsonResponse({"error": "Email is required"}, status=400)

            # ✅ Send Email via Logic App
            payload = {
                "email": recipient,
                "subject": subject,
                "message": message
            }
            response = requests.post(LOGIC_APP_URL, json=payload)

            if response.status_code == 200:
                return JsonResponse({"success": True, "message": "Email sent successfully"})
            else:
                return JsonResponse({"error": "Failed to send email"}, status=response.status_code)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .signals import log_failed_login  # Import this!

def custom_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # or wherever
        else:
            ip = request.META.get("REMOTE_ADDR")
            log_failed_login(username, ip)  # ✅ Call this on failure
            messages.error(request, "Invalid login credentials.")
    return render(request, "login.html")


import logging
import json
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now

logger = logging.getLogger("django")

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log_data = {
        "Username": user.username,
        "Status": "Success",
        "IP": get_client_ip(request),
        "Timestamp": now().isoformat()
    }
    logger.info(json.dumps(log_data))  # ✅ Directly log flat JSON

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_data = {
        "Username": user.username,
        "Status": "Logout",
        "IP": get_client_ip(request),
        "Timestamp": now().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_failed_login(username, ip):
    log_data = {
        "Username": username,
        "Status": "Failed",
        "IP": ip,
        "Timestamp": now().isoformat()
    }
    logger.warning(json.dumps(log_data))

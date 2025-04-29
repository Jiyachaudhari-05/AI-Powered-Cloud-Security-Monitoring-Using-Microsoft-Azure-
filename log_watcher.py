import json
import datetime
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging

logger = logging.getLogger("django_login_logs")

class LoginActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            log_data = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "user": request.user.username,
                "ip_address": self.get_client_ip(request),
                "event": "login_attempt",
            }
            logger.info(json.dumps(log_data))

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user": user.username,
        "ip_address": request.META.get("REMOTE_ADDR"),
        "event": "user_logged_in",
    }
    logger.info(json.dumps(log_data))

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user": user.username,
        "ip_address": request.META.get("REMOTE_ADDR"),
        "event": "user_logged_out",
    }
    logger.info(json.dumps(log_data))

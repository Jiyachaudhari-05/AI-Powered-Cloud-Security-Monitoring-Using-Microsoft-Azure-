# views.py
import logging
from django.http import HttpResponse

# Get the logger defined in settings.py
logger = logging.getLogger('django')

def test_logging(request):
    # Log some messages
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")

    return HttpResponse("Logging test completed. Check your logs.")

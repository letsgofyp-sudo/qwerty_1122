import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django application
app = get_wsgi_application()

def handler(event, context):
    from django.core.handlers.wsgi import WSGIHandler
    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    
    # Ensure settings are configured
    if not settings.configured:
        settings.configure()
    
    # Get the WSGI application
    wsgi_application = get_wsgi_application()
    
    # Handle the request
    response = wsgi_application(event, context)
    
    return response

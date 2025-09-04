import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django application
application = get_wsgi_application()

def handler(event, context):
    from io import BytesIO
    import json
    
    # Create a simple response for now
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'status': 'ok', 'message': 'Django is running on Vercel'})
    }

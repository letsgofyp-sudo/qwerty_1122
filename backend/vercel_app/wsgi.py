import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django application
application = get_wsgi_application()

def handler(request, context):
    from django.core.handlers.wsgi import WSGIHandler
    from django.core.handlers.wsgi import WSGIRequest
    from django.core.handlers.wsgi import WSGIHandler
    from django.core.handlers import base
    from django.http import HttpResponse
    from io import BytesIO
    import json
    
    # Create a WSGI environment from the Vercel request
    environ = {
        'REQUEST_METHOD': request['httpMethod'],
        'PATH_INFO': request['path'],
        'QUERY_STRING': request.get('queryStringParameters', '') or '',
        'SERVER_NAME': request['headers'].get('host', ''),
        'SERVER_PORT': request['headers'].get('x-forwarded-port', '80'),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.url_scheme': request['headers'].get('x-forwarded-proto', 'http'),
        'wsgi.input': BytesIO(json.dumps(request.get('body', '')).encode() if request.get('body') else b''),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': True,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to the environment
    for key, value in request['headers'].items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value
    
    # Handle the request
    response = application(environ, lambda status, headers: None)
    
    # Convert the response to the format expected by Vercel
    response_body = b''.join(response)
    
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response_body.decode('utf-8')
    }

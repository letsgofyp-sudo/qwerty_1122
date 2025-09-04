import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django application
application = get_wsgi_application()

def handler(event, context):
    from django.core.handlers.wsgi import WSGIRequest
    from io import BytesIO
    import json
    
    # Create a WSGI environment from the Vercel request
    environ = {
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', '') or '',
        'SERVER_NAME': event['headers'].get('host', ''),
        'SERVER_PORT': event['headers'].get('x-forwarded-port', '80'),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.url_scheme': event['headers'].get('x-forwarded-proto', 'http'),
        'wsgi.input': BytesIO(json.dumps(event.get('body', '')).encode() if event.get('body') else b''),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': True,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to the environment
    if 'headers' in event:
        for key, value in event['headers'].items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value
    
    # Handle the request
    response = {}
    
    def start_response(status, response_headers, exc_info=None):
        nonlocal response
        response['statusCode'] = int(status.split(' ')[0])
        response['headers'] = dict(response_headers)
        return lambda body: None
    
    response_body = application(environ, start_response)
    
    if 'statusCode' not in response:
        response['statusCode'] = 500
        response['body'] = 'Internal Server Error'
    else:
        response['body'] = b''.join(response_body).decode('utf-8')
    
    return response

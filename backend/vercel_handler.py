from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import sys

def handler(event, context):
    # Add the project directory to the Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    try:
        from django.core.wsgi import get_wsgi_application
        from django.core.handlers.wsgi import WSGIHandler
        from django.core.handlers.wsgi import WSGIRequest
        from io import BytesIO
    except ImportError as e:
        return {
            'statusCode': 500,
            'body': f'Django import error: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }
    
    try:
        # Initialize Django application
        application = get_wsgi_application()
        
        # Parse the event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '')
        query_params = event.get('queryStringParameters', {}) or {}
        
        # Build the WSGI environment
        environ = {
            'REQUEST_METHOD': http_method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_params.items()]) if query_params else '',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': headers.get('x-forwarded-proto', 'http'),
            'wsgi.input': BytesIO(body.encode() if isinstance(body, str) else body or b''),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'SERVER_NAME': headers.get('host', ''),
            'SERVER_PORT': headers.get('x-forwarded-port', '80'),
        }
        
        # Add headers to the environment
        for key, value in headers.items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value
        
        # Handle the request
        response_headers = {}
        response_body = []
        
        def start_response(status, headers, exc_info=None):
            nonlocal response_headers
            response_headers['status'] = status
            response_headers['headers'] = dict(headers)
            return response_body.append
        
        result = application(environ, start_response)
        
        # Combine the response body
        if not response_body and hasattr(result, '__iter__'):
            response_body = [chunk for chunk in result]
        
        # Build the response
        status_code = int(response_headers.get('status', '200').split()[0])
        headers = response_headers.get('headers', {})
        
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': b''.join(response_body).decode('utf-8') if response_body else ''
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }

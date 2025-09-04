from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json

def handler(event, context):
    try:
        return {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'status': 'success',
                'message': 'Hello from Vercel!',
                'path': event.get('path', '/')
            })
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

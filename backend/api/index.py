import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Prepare the response
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'status': 'success',
                'message': 'API is working!',
                'path': event.get('path', '/'),
                'httpMethod': event.get('httpMethod', 'GET')
            })
        }
        
        # Log the response
        logger.info(f"Sending response: {json.dumps(response)}")
        return response
        
    except Exception as e:
        # Log the error
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'error',
                'message': 'Internal server error',
                'error': str(e)
            })
        }

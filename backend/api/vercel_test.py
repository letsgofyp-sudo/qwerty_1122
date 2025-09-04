def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status": "success", "message": "Vercel test endpoint is working!"}'
    }

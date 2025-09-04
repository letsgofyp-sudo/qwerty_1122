import requests
import os
import logging
from requests.exceptions import HTTPError, Timeout

# Set up logging
logger = logging.getLogger(__name__)

# Load TextBee configuration from environment variables with error handling
try:
    BASE_URL = os.environ.get('TEXTBEE_BASE_URL')
    API_KEY = os.environ.get('TEXTBEE_API_KEY')
    DEVICE_ID = os.environ.get('TEXTBEE_DEVICE_ID')
    
    if not all([BASE_URL, API_KEY, DEVICE_ID]):
        logger.warning("One or more TextBee environment variables are missing. SMS functionality will be disabled.")
        TEXTBEE_ENABLED = False
    else:
        TEXTBEE_ENABLED = True
        
except Exception as e:
    logger.error(f"Error loading TextBee configuration: {e}")
    TEXTBEE_ENABLED = False

# Endpoint path template
SEND_SMS_PATH = "/api/v1/gateway/devices/{device_id}/send-sms"

def send_phone_otp(phone_number: str, otp_code: str) -> bool:
    """
    Send a single SMS via TextBee.
    :param phone_number: E.164 format, e.g. "+923316963802"
    :param otp_code: The OTP code to send, e.g. "3453"
    :returns: True if SMS was sent or if TextBee is not configured, False on failure.
    """
    if not TEXTBEE_ENABLED:
        logger.warning("TextBee is not configured. SMS not sent.")
        return True  # Return True to allow the registration flow to continue

    logger.info(f"Sending OTP {otp_code} to {phone_number}")
    
    try:
        url = f"{BASE_URL}{SEND_SMS_PATH.format(device_id=DEVICE_ID)}"
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "recipients": [phone_number],
            "message": f"Your OTP is {otp_code}",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        logger.info(f"SMS sent successfully to {phone_number}")
        return True
        
    except HTTPError as err:
        logger.error(f"HTTP error sending SMS: {err} - Response: {getattr(err, 'response', {}).text}")
    except Timeout:
        logger.error("Timeout while sending SMS")
    except Exception as err:
        logger.error(f"Unexpected error sending SMS: {err}")
        
    return False
    

def send_phone_otp_for_reset(phone_number: str, otp_code: str) -> bool:
    """
    Sends a password reset OTP via SMS using TextBee.
    :param phone_number: E.164 format phone number
    :param otp_code: The OTP code to send
    :returns: True if SMS was sent or if TextBee is not configured, False on failure
    """
    if not TEXTBEE_ENABLED:
        logger.warning("TextBee is not configured. Password reset SMS not sent.")
        return True  # Return True to allow the password reset flow to continue
        
    logger.info(f"Sending password reset OTP {otp_code} to {phone_number}")
    
    try:
        url = f"{BASE_URL}{SEND_SMS_PATH.format(device_id=DEVICE_ID)}"
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "recipients": [phone_number],
            "message": f"Your password reset OTP is {otp_code}",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        logger.info(f"Password reset SMS sent successfully to {phone_number}")
        return True
        
    except HTTPError as err:
        logger.error(f"HTTP error sending password reset SMS: {err} - Response: {getattr(err, 'response', {}).text}")
    except Timeout:
        logger.error("Timeout while sending password reset SMS")
    except Exception as err:
        logger.error(f"Unexpected error sending password reset SMS: {err}")
        
    return False

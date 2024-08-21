from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, Exception):
            logger.error(f"Unhandled exception: {exc}", exc_info=True)
            response = Response({
                'code': 500,
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=500)
    
    return response


class CustomValidationError(APIException):
    status_code = 400  
    default_code = '400'

    def __init__(self, code=None, message=None):
        if code is None:
            code = self.default_code
        if message is None:
            message = "Invalid input."
        self.detail = {
            'code': code,
            'message': message
        }
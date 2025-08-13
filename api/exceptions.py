from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from api.utils import CustomResponse
from api.constants import MessageCodes


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return standardized error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Convert DRF's default error response to our custom format
        return CustomResponse.error(
            message_code=MessageCodes.VALIDATION_ERROR,
            data=response.data,
            status_code=response.status_code
        )
    
    # Handle unexpected exceptions
    return CustomResponse.server_error(
        MessageCodes.SERVER_ERROR,
        {'detail': str(exc)}
    ) 
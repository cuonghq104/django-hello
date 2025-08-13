from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    """
    Custom response class to standardize API responses
    """
    
    @staticmethod
    def success(data=None, message_code="OK", status_code=status.HTTP_200_OK):
        """
        Return a successful response
        """
        return Response({
            'success': True,
            'code': status_code,
            'message': message_code,
            'data': data
        }, status=status_code)
    
    @staticmethod
    def error(message_code="ERROR", data=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Return an error response
        """
        return Response({
            'success': False,
            'code': status_code,
            'message': message_code,
            'data': data
        }, status=status_code)
    
    @staticmethod
    def created(data=None, message_code="CREATED"):
        """
        Return a created response (201)
        """
        return CustomResponse.success(data, message_code, status.HTTP_201_CREATED)
    
    @staticmethod
    def not_found(message_code="NOT_FOUND", data=None):
        """
        Return a not found response (404)
        """
        return CustomResponse.error(message_code, data, status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def unauthorized(message_code="UNAUTHORIZED", data=None):
        """
        Return an unauthorized response (401)
        """
        return CustomResponse.error(message_code, data, status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(message_code="FORBIDDEN", data=None):
        """
        Return a forbidden response (403)
        """
        return CustomResponse.error(message_code, data, status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def validation_error(message_code="VALIDATION_ERROR", data=None):
        """
        Return a validation error response (400)
        """
        return CustomResponse.error(message_code, data, status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def server_error(message_code="SERVER_ERROR", data=None):
        """
        Return a server error response (500)
        """
        return CustomResponse.error(message_code, data, status.HTTP_500_INTERNAL_SERVER_ERROR) 
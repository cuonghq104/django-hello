from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
import csv

from api.models import Store
from api.permissions.store_permissions import IsStoreOwner
from api.serializers import StoreSerializer, StoreCreateSerializer, StoreProductBulkCreateSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.annotate(products_count=Count('products'))
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'delete':
            self.permission_classes = [IsAdminUser]
        elif self.action == 'update':
            self.permission_classes = [IsAdminUser, IsStoreOwner]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return StoreCreateSerializer
        elif self.action == 'bulk_create_product':
            return StoreProductBulkCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Bulk create products for a store",
        description="Upload a file to bulk create products for a specific store. Currently just tests file upload functionality.",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'integer',
                        'description': 'Store ID where products will be created',
                        'minimum': 1
                    },
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'File to upload (CSV, Excel, etc.)'
                    }
                },
                'required': ['id', 'file']
            }
        },
        responses={
            200: {
                'description': 'File uploaded successfully',
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'store_id': {'type': 'integer'},
                    'file_name': {'type': 'string'},
                    'file_size': {'type': 'integer'}
                }
            },
            400: {
                'description': 'Bad request - invalid data'
            }
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    'message': 'File uploaded successfully',
                    'store_id': 1,
                    'file_name': 'products.csv',
                    'file_size': 1024
                },
                response_only=True,
                status_codes=['200']
            )
        ]
    )
    @action(detail=False, methods=['post'], name='bulk_create_product', url_path='bulk_create_product',
            parser_classes=[MultiPartParser])
    def bulk_create_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            store_id = serializer.validated_data['id']
            uploaded_file = serializer.validated_data['file']

            # Decode the uploaded file content to text
            try:
                # Read the file content and decode it to text
                file_content = uploaded_file.read().decode('utf-8')
                uploaded_file.seek(0)  # Reset file pointer for potential future reads
                
                # Create CSV reader from the decoded text content
                reader = csv.reader(file_content.splitlines())
                for row in reader:
                    print(row)

                # For now, just return success response to test file upload
                response_data = {
                    'message': 'File uploaded successfully',
                    'store_id': store_id,
                    'file_name': uploaded_file.name,
                    'file_size': uploaded_file.size
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            except UnicodeDecodeError:
                return Response(
                    {'error': 'Invalid file encoding. Please ensure the file is UTF-8 encoded.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

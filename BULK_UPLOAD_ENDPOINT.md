# Bulk Create Product Endpoint

## Overview
The `bulk_create_product` endpoint allows you to upload a file to bulk create products for a specific store. Currently, this endpoint is set up to test file upload functionality.

## Endpoint Details
- **URL**: `/stores/bulk_create_product/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Required (IsAuthenticated)

## Request Parameters

### Form Data
- `id` (integer, required): The store ID where products will be created
- `file` (file, required): The file to upload (any file type is accepted for now)

## Response Format

### Success Response (200)
```json
{
    "message": "File uploaded successfully",
    "store_id": 1,
    "file_name": "products.csv",
    "file_size": 1024
}
```

### Error Response (400)
```json
{
    "id": ["This field is required."],
    "file": ["This field is required."]
}
```

## Testing the Endpoint

### Using Swagger UI
1. Start your Django server: `python manage.py runserver`
2. Navigate to: `http://localhost:8000/api/schema/swagger-ui/`
3. Find the `bulk_create_product` endpoint under the stores section
4. Click "Try it out"
5. Fill in the form:
   - `id`: Enter a store ID (e.g., 1)
   - `file`: Upload any file
6. Click "Execute"

### Using cURL
```bash
curl -X POST "http://localhost:8000/stores/bulk_create_product/" \
  -H "Content-Type: multipart/form-data" \
  -F "id=1" \
  -F "file=@your_file.csv"
```

### Using Python requests
```python
import requests

url = 'http://localhost:8000/stores/bulk_create_product/'
files = {'file': open('your_file.csv', 'rb')}
data = {'id': 1}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Using the test script
```bash
python3 test_bulk_upload.py
```

## Implementation Notes

### Current Implementation
- The endpoint currently only validates and returns file information
- No actual product creation logic is implemented yet
- File content is not processed

### Future Enhancements
- Parse CSV/Excel files to extract product data
- Validate product data against the Product model
- Create Product instances in the database
- Handle bulk operations with transaction support
- Add support for different file formats

### Files Modified
1. `api/serializers/store_serializers.py` - Added `StoreProductBulkCreateSerializer`
2. `api/serializers/__init__.py` - Exported the new serializer
3. `api/views/store_views.py` - Implemented the endpoint with Swagger documentation
4. `drf_course/settings.py` - Added media file configurations
5. `drf_course/urls.py` - Added media file serving for development

## Security Considerations
- File upload validation should be added in production
- File size limits should be configured
- File type validation should be implemented
- Authentication and authorization should be properly configured


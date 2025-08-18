#!/usr/bin/env python3
"""
Test script for the bulk_create_product endpoint
This script demonstrates how to upload a file to the endpoint
"""

import requests
import os

# Create a test file
def create_test_file():
    """Create a simple test file for upload"""
    test_content = "product_name,description,price,stock\n"
    test_content += "Test Product 1,This is a test product,19.99,100\n"
    test_content += "Test Product 2,Another test product,29.99,50\n"
    
    with open('test_products.csv', 'w') as f:
        f.write(test_content)
    
    return 'test_products.csv'

def test_bulk_upload():
    """Test the bulk_create_product endpoint"""
    
    # Create test file
    filename = create_test_file()
    
    # API endpoint URL (adjust the base URL as needed)
    url = 'http://localhost:8000/stores/bulk_create_product/'
    
    # Prepare the multipart form data
    files = {
        'file': ('test_products.csv', open(filename, 'rb'), 'text/csv')
    }
    
    data = {
        'id': 1  # Store ID
    }
    
    try:
        # Make the POST request
        response = requests.post(url, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ File upload successful!")
        else:
            print("❌ File upload failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up test file
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    print("Testing bulk_create_product endpoint...")
    test_bulk_upload()


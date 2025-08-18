#!/usr/bin/env python3
"""
Simple test script to verify file upload functionality
"""

import requests
import os

def test_file_upload():
    """Test the file upload endpoint"""
    
    # Create a simple test file
    test_content = "test,data,here\n1,2,3\n"
    with open('test_file.csv', 'w') as f:
        f.write(test_content)
    
    try:
        # Test the endpoint
        url = 'http://localhost:8000/stores/bulk_create_product/'
        
        with open('test_file.csv', 'rb') as f:
            files = {'file': ('test_file.csv', f, 'text/csv')}
            data = {'id': 1}
            
            response = requests.post(url, files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ File upload test successful!")
            else:
                print("❌ File upload test failed!")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        if os.path.exists('test_file.csv'):
            os.remove('test_file.csv')

if __name__ == "__main__":
    print("Testing file upload endpoint...")
    test_file_upload()


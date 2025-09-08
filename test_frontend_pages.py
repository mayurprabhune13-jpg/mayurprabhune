#!/usr/bin/env python3
"""
Script to test all frontend pages and API endpoints.
"""
import requests
from bs4 import BeautifulSoup
import json

# Base URL
BASE_URL = "http://localhost:5000"

def test_public_pages():
    """Test all public frontend pages without authentication"""
    pages_to_test = [
        "/",           # Home page
        "/about",      # About page
        "/services",   # Services page
        "/contact",    # Contact page
        "/videos",     # Videos listing
        "/testimonials", # Testimonials page
        "/blog",       # Blog listing
        "/success-stories" # Case studies page
    ]
    
    print("Testing public frontend pages...")
    session = requests.Session()
    
    for page in pages_to_test:
        try:
            response = session.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✓ {page} - OK (200)")
                # Basic content check
                if "html" in response.text.lower():
                    print(f"  Content: HTML detected")
                else:
                    print(f"  Warning: No HTML content found")
            else:
                print(f"✗ {page} - Failed ({response.status_code})")
        except Exception as e:
            print(f"✗ {page} - Error: {str(e)}")

def test_api_endpoints():
    """Test API endpoints after authentication"""
    print("\nTesting API endpoints after authentication...")
    
    # First, login to get authenticated session
    session = requests.Session()
    
    # Get login page to extract CSRF token
    login_page = session.get(f"{BASE_URL}/auth/login")
    if login_page.status_code != 200:
        print("Failed to get login page")
        return False
    
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_input:
        print("CSRF token not found")
        return False
    
    csrf_token = csrf_input.get('value')
    
    # Login credentials
    login_data = {
        'username': 'admin',
        'password': 'adminpass123',
        'csrf_token': csrf_token
    }
    
    # Login
    login_response = session.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if login_response.status_code != 200:
        print("Login failed")
        return False
    
    # Test API endpoints
    api_endpoints = [
        "/api/videos",
        "/api/posts", 
        "/api/case-studies",
        "/api/testimonials",
        "/api/messages",
        "/api/stats"
    ]
    
    for endpoint in api_endpoints:
        try:
            response = session.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✓ {endpoint} - OK (200)")
                try:
                    data = response.json()
                    print(f"  Data: {len(data)} items returned" if isinstance(data, list) else "  JSON response received")
                except:
                    print(f"  Response: {response.text[:100]}...")
            elif response.status_code == 403:
                print(f"✗ {endpoint} - Access denied (403) - Check admin privileges")
            else:
                print(f"✗ {endpoint} - Failed ({response.status_code})")
        except Exception as e:
            print(f"✗ {endpoint} - Error: {str(e)}")

def test_contact_form():
    """Test contact form submission"""
    print("\nTesting contact form submission...")
    
    session = requests.Session()
    
    # Get contact page to extract CSRF token
    contact_page = session.get(f"{BASE_URL}/contact")
    if contact_page.status_code != 200:
        print("Failed to get contact page")
        return False
    
    soup = BeautifulSoup(contact_page.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_input:
        print("CSRF token not found in contact form")
        return False
    
    csrf_token = csrf_input.get('value')
    
    # Test contact form submission
    contact_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'This is a test message from the automated test script.',
        'csrf_token': csrf_token
    }
    
    try:
        response = session.post(f"{BASE_URL}/contact", data=contact_data)
        if response.status_code == 200 or response.status_code == 302:
            print("✓ Contact form submission - OK")
            if "success" in response.text.lower() or "flash" in response.text.lower():
                print("  Success message detected")
        else:
            print(f"✗ Contact form submission - Failed ({response.status_code})")
    except Exception as e:
        print(f"✗ Contact form submission - Error: {str(e)}")

if __name__ == '__main__':
    print("Starting comprehensive frontend and API tests...")
    print("=" * 50)
    
    # Test public pages
    test_public_pages()
    
    # Test API endpoints (requires authentication)
    test_api_endpoints()
    
    # Test contact form
    test_contact_form()
    
    print("\n" + "=" * 50)
    print("Test completed!")
#!/usr/bin/env python3
"""
Script to test admin login functionality.
"""
import requests
from bs4 import BeautifulSoup

# Base URL
BASE_URL = "http://localhost:5000"

def test_login():
    # Create a session to maintain cookies
    session = requests.Session()
    
    # First, get the login page to extract CSRF token
    login_page = session.get(f"{BASE_URL}/auth/login")
    if login_page.status_code != 200:
        print(f"Failed to get login page. Status: {login_page.status_code}")
        return False
    
    # Parse the HTML to find CSRF token
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_input:
        print("CSRF token not found in login form")
        return False
    
    csrf_token = csrf_input.get('value')
    print(f"CSRF Token: {csrf_token}")
    
    # Login credentials
    login_data = {
        'username': 'admin',
        'password': 'adminpass123',
        'csrf_token': csrf_token
    }
    
    # Attempt login
    login_response = session.post(f"{BASE_URL}/auth/login", data=login_data)
    
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response URL: {login_response.url}")
    print(f"Login response cookies: {login_response.cookies}")
    print(f"Session cookies: {session.cookies}")
    
    # Check if login was successful (should redirect to home page)
    if login_response.status_code == 200:
        # After login, try to access admin dashboard to confirm authentication
        dashboard_response = session.get(f"{BASE_URL}/admin/dashboard")
        print(f"Dashboard response status: {dashboard_response.status_code}")
        print(f"Dashboard response URL: {dashboard_response.url}")
        print(f"Dashboard response text: {dashboard_response.text[:200]}")  # First 200 chars for error details
        
        if dashboard_response.status_code == 200 and "dashboard" in dashboard_response.url:
            print("Login successful! Redirected to admin dashboard.")
            return True
        else:
            print("Login may have failed - check response content:")
            print(login_response.text[:500])  # First 500 chars
            print("Dashboard access failed - may not be authenticated")
            return False
    else:
        print("Login failed with status code:", login_response.status_code)
        return False

if __name__ == '__main__':
    success = test_login()
    if success:
        print("Login test passed!")
    else:
        print("Login test failed!")
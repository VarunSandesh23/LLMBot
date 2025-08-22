#!/usr/bin/env python3
"""
Test script for Google Gemini API integration
"""

import google.generativeai as genai

# Configure the API
genai.configure(api_key='AIzaSyDY7hbsK8pVPSG-i08-eed21m5bmxYPzQU')

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Test prompt
response = model.generate_content('Hello! Tell me a joke.')

print('Response:', response.text)

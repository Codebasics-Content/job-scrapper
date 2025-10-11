#!/usr/bin/env python3
"""
BrightData Dataset Discovery Script
====================================
This script helps you discover what datasets are available in YOUR BrightData account.
It will list all datasets you have access to with their correct IDs.

Usage:
    python check_brightdata_datasets.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_brightdata_account():
    """Check BrightData account and list available datasets."""
    
    api_token = os.getenv("BRIGHTDATA_API_TOKEN")
    
    if not api_token:
        print("❌ Error: BRIGHTDATA_API_TOKEN not found in .env file")
        return
    
    print("🔍 Checking BrightData Account...")
    print(f"API Token: {api_token[:20]}...{api_token[-10:]}")
    print("-" * 60)
    
    # BrightData API base URL
    base_url = "https://api.brightdata.com"
    
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Try different endpoints to discover datasets
    endpoints_to_try = [
        ("/datasets/v3", "List all datasets (v3)"),
        ("/datasets", "List all datasets"),
        ("/dca/datasets", "List DCA datasets"),
        ("/account", "Account information"),
    ]
    
    print("\n📡 Testing API Endpoints...\n")
    
    for endpoint, description in endpoints_to_try:
        url = f"{base_url}{endpoint}"
        print(f"Testing: {description}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Success!")
                data = response.json()
                print(f"Response: {data}")
                print("\n" + "=" * 60 + "\n")
            elif response.status_code == 401:
                print("❌ Unauthorized - API token may be invalid")
                print(f"Response: {response.text}")
                print("\n" + "=" * 60 + "\n")
                break  # No point trying other endpoints
            elif response.status_code == 404:
                print("⚠️  Endpoint not found")
                print(f"Response: {response.text}")
                print("\n" + "=" * 60 + "\n")
            else:
                print(f"⚠️  Status {response.status_code}")
                print(f"Response: {response.text}")
                print("\n" + "=" * 60 + "\n")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            print("\n" + "=" * 60 + "\n")
    
    print("\n📋 Summary")
    print("-" * 60)
    print("\nBased on the responses above:")
    print("1. If you see '401 Unauthorized' - your API token is invalid")
    print("2. If you see '404 Not Found' - the endpoint doesn't exist or you don't have access")
    print("3. If you see '200 Success' - check the response for your dataset IDs")
    
    print("\n🔧 Next Steps:")
    print("-" * 60)
    print("\nOption A: Check BrightData Dashboard")
    print("   1. Login to: https://brightdata.com/cp/dashboard")
    print("   2. Go to 'Datasets' or 'Data Collector' section")
    print("   3. Look for your dataset IDs (format: gd_XXXXX)")
    print("   4. Update src/scraper/brightdata/config/settings.py with YOUR IDs")
    
    print("\nOption B: Contact BrightData Support")
    print("   1. Ask for your account's dataset IDs")
    print("   2. Confirm API access is enabled for datasets")
    print("   3. Verify your subscription includes LinkedIn/Indeed datasets")
    
    print("\nOption C: Use Naukri Instead (RECOMMENDED)")
    print("   ✅ Works immediately without BrightData setup")
    print("   ✅ Already integrated and tested")
    print("   ✅ No additional configuration needed")
    print("   Command: streamlit run streamlit_app.py")
    print("   Select: Naukri platform")
    
    print("\n" + "=" * 60)

def test_specific_dataset(dataset_id: str):
    """Test access to a specific dataset ID."""
    
    api_token = os.getenv("BRIGHTDATA_API_TOKEN")
    
    if not api_token:
        print("❌ Error: BRIGHTDATA_API_TOKEN not found")
        return
    
    base_url = "https://api.brightdata.com"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Try to get dataset info
    url = f"{base_url}/datasets/v3/{dataset_id}"
    
    print(f"\n🔍 Testing Dataset: {dataset_id}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dataset accessible!")
            data = response.json()
            print(f"Dataset Info: {data}")
        elif response.status_code == 404:
            print("❌ Dataset not found or not accessible with your account")
            print("This dataset ID does not exist in your BrightData account")
        elif response.status_code == 401:
            print("❌ Unauthorized - check your API token")
        else:
            print(f"⚠️  Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("BrightData Dataset Discovery Tool")
    print("=" * 60)
    
    # Check account first
    check_brightdata_account()
    
    # Test the configured dataset IDs
    print("\n" + "=" * 60)
    print("Testing Configured Dataset IDs")
    print("=" * 60)
    
    test_specific_dataset("gd_lpfll7v5hcqtkxl6l")  # LinkedIn
    test_specific_dataset("gd_l4dx9j9sscpvs7no2")  # Indeed
    
    print("\n" + "=" * 60)
    print("✅ Discovery Complete!")
    print("=" * 60)
    print("\nIf you see 404 errors above, these dataset IDs don't exist in your account.")
    print("You need to either:")
    print("  1. Create these datasets in BrightData dashboard")
    print("  2. Find your existing dataset IDs and update settings.py")
    print("  3. Use Naukri scraper instead (works immediately)")
    print("\nRecommendation: 🎯 Use Naukri for now!")

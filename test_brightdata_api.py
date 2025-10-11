#!/usr/bin/env python3
"""
BrightData API Diagnostic Tool
Tests API access and discovers available datasets
"""
import sys
import requests
sys.path.insert(0, 'src')

from scraper.brightdata.config.settings import get_settings

def test_brightdata_api():
    """Test BrightData API and list available datasets."""
    settings = get_settings()
    
    # Prepare headers
    token = settings.api_token
    if not token.startswith("Bearer"):
        token = f"Bearer {token}"
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    
    print("=" * 70)
    print("BrightData API Diagnostic Tool")
    print("=" * 70)
    print(f"\nAPI Token: {settings.api_token[:20]}...")
    print(f"Base URL: {settings.base_url}")
    
    # Test 1: Try to list datasets
    print("\n" + "=" * 70)
    print("Test 1: Discovering Available Datasets")
    print("=" * 70)
    
    endpoints_to_try = [
        "/datasets/v3",
        "/dca/datasets",
        "/datasets",
    ]
    
    for endpoint in endpoints_to_try:
        url = f"{settings.base_url}{endpoint}"
        print(f"\n📡 GET {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Success!")
                data = response.json()
                print(f"   Response: {data}")
                
                # Try to extract dataset IDs
                if isinstance(data, list):
                    print(f"\n   Found {len(data)} datasets:")
                    for ds in data[:10]:  # Show first 10
                        if isinstance(ds, dict):
                            ds_id = ds.get('id') or ds.get('dataset_id') or ds.get('_id')
                            ds_name = ds.get('name') or ds.get('title')
                            print(f"      - {ds_id}: {ds_name}")
                elif isinstance(data, dict) and 'datasets' in data:
                    print(f"\n   Found {len(data['datasets'])} datasets:")
                    for ds in data['datasets'][:10]:
                        ds_id = ds.get('id') or ds.get('dataset_id')
                        ds_name = ds.get('name') or ds.get('title')
                        print(f"      - {ds_id}: {ds_name}")
                break  # Success, no need to try other endpoints
            else:
                print(f"   ❌ {response.status_code}: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 2: Test the configured dataset IDs
    print("\n" + "=" * 70)
    print("Test 2: Testing Configured Dataset IDs")
    print("=" * 70)
    
    datasets_to_test = [
        ("LinkedIn", settings.linkedin_dataset_id),
        ("Indeed", settings.indeed_dataset_id),
    ]
    
    for name, dataset_id in datasets_to_test:
        print(f"\n📊 {name} Dataset: {dataset_id}")
        
        # Try to trigger a minimal collection
        trigger_url = f"{settings.base_url}/datasets/v3/trigger"
        params = {
            "dataset_id": dataset_id,
            "include_errors": "true",
            "type": "discover_new",
            "discover_by": "keyword",
        }
        data = {
            "input": [{"keyword": "test", "location": "US"}],
            "limit": 1
        }
        
        print(f"   POST {trigger_url}")
        try:
            response = requests.post(trigger_url, headers=headers, params=params, json=data, timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Trigger successful!")
                print(f"   Snapshot ID: {result.get('snapshot_id')}")
            else:
                print(f"   ❌ Error: {response.text}")
                
                # Check if it's an authentication or dataset access issue
                if "not found" in response.text.lower() or "404" in str(response.status_code):
                    print(f"   💡 Dataset {dataset_id} not found in your account")
                elif "unauthorized" in response.text.lower() or "401" in str(response.status_code):
                    print(f"   💡 API token doesn't have access to this dataset")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Test API token validity
    print("\n" + "=" * 70)
    print("Test 3: API Token Validation")
    print("=" * 70)
    
    test_url = f"{settings.base_url}/datasets/v3"
    print(f"\n📡 GET {test_url}")
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print("   ❌ API token is invalid or unauthorized")
            print("   💡 Get a valid token from: https://brightdata.com/cp/datasets")
        elif response.status_code == 200:
            print("   ✅ API token is valid!")
        else:
            print(f"   ⚠️  Unexpected status: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Diagnostic Complete")
    print("=" * 70)
    print("\n💡 Next Steps:")
    print("   1. If dataset IDs are not found, you need to create them in BrightData dashboard")
    print("   2. Go to: https://brightdata.com/cp/datasets")
    print("   3. Create 'LinkedIn Jobs' and 'Indeed Jobs' datasets")
    print("   4. Copy the dataset IDs and update settings.py")
    print("   5. Or use the dataset IDs discovered above")
    print()

if __name__ == "__main__":
    test_brightdata_api()

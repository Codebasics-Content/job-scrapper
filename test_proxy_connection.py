"""Test BrightData proxy connection extracted from Browser URL.

This script verifies that:
1. Credentials are extracted from BRIGHTDATA_BROWSER_URL
2. Proxy connection works
3. We get a response through BrightData's network
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, 'src')

from scraper.proxy.config import BrightDataProxy, ProxySession


async def test_proxy_connection():
    """Test BrightData proxy connection."""
    
    print("\n" + "="*60)
    print("🧪 Testing BrightData Proxy Connection")
    print("="*60)
    
    # Load environment
    load_dotenv()
    
    print("\n📋 Step 1: Loading credentials...")
    try:
        proxy = BrightDataProxy.from_env()
        print(f"   ✅ Customer ID: {proxy.customer_id}")
        print(f"   ✅ Zone: {proxy.zone_name}")
        print(f"   ✅ Password: {proxy.password[:4]}{'*' * (len(proxy.password) - 4)}")
    except Exception as e:
        print(f"   ❌ Failed to load credentials: {e}")
        return False
    
    print("\n📋 Step 2: Testing proxy connection...")
    print(f"   Proxy URL: {proxy.url[:50]}...")
    
    # Create session
    session = ProxySession(timeout=30.0)
    
    # Test with httpbin (shows your IP)
    test_url = "https://httpbin.org/ip"
    
    try:
        print(f"   Making request to {test_url}...")
        response = await session.get(test_url, proxies=proxy.auth_dict)
        
        if response.status_code == 200:
            data = response.json()
            ip_address = data.get("origin", "Unknown")
            
            print(f"\n✅ SUCCESS! Proxy connection working!")
            print(f"   Status: {response.status_code}")
            print(f"   Your IP through proxy: {ip_address}")
            print(f"   Response: {response.text[:100]}...")
            
            # Test with a real site
            print(f"\n📋 Step 3: Testing with real job site (LinkedIn)...")
            test_url2 = "https://www.linkedin.com"
            
            try:
                response2 = await session.get(test_url2, proxies=proxy.auth_dict)
                print(f"   ✅ LinkedIn response: {response2.status_code}")
                print(f"   Content length: {len(response2.text)} chars")
                
                if "linkedin" in response2.text.lower():
                    print(f"   ✅ Successfully fetched LinkedIn content!")
                else:
                    print(f"   ⚠️  Got response but content may be unexpected")
                    
            except Exception as e:
                print(f"   ⚠️  LinkedIn test failed: {e}")
                print(f"   This is okay - might be rate limiting")
            
            return True
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    success = await test_proxy_connection()
    
    print("\n" + "="*60)
    if success:
        print("✅ All tests passed! Your proxy is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: python3 src/scraper/proxy/linkedin_scraper.py")
        print("   2. Run: python3 src/scraper/proxy/indeed_scraper.py")
        print("   3. Run: python3 src/scraper/proxy/naukri_scraper.py")
    else:
        print("❌ Tests failed. Check your credentials and try again.")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify BRIGHTDATA_BROWSER_URL in .env")
        print("   2. Check BrightData dashboard for active zones")
        print("   3. Ensure you have bandwidth available")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

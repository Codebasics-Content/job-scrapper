"""Test BrightData proxy connection directly"""
import urllib.request
import ssl
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

proxy_url = os.getenv("PROXY_URL")
print(f"Testing proxy: {proxy_url[:50]}...")

# Create SSL context that doesn't verify certificates (for proxy testing)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Test proxy connection
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({
        'http': proxy_url,
        'https': proxy_url
    }),
    urllib.request.HTTPSHandler(context=ssl_context)
)

try:
    response = opener.open('https://geo.brdtest.com/mygeo.json')
    result = response.read().decode('utf-8')
    print(f"\n✅ Proxy connection successful!")
    print(f"Response: {result}")
except Exception as e:
    print(f"\n❌ Proxy connection failed: {e}")

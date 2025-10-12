#!/usr/bin/env python3
"""Direct proxy test with fresh environment"""
import os
from dotenv import load_dotenv

# Force reload .env
load_dotenv(override=True)

proxy_url = os.getenv("PROXY_URL")
print(f"Proxy from .env: {proxy_url}")

# Test with requests
import requests

try:
    response = requests.get(
        "https://lumtest.com/myip.json",
        proxies={"https": proxy_url, "http": proxy_url},
        timeout=30
    )
    print(f"\n✅ SUCCESS! Proxy working!")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"\n❌ FAILED: {e}")

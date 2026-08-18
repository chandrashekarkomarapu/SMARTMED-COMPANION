#!/usr/bin/env python
"""Test dashboard endpoint after fixes."""

import httpx
import sys

client = httpx.Client()
try:
    response = client.get("http://localhost:8000/dashboard", follow_redirects=True)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)} bytes")
    
    if response.status_code == 200:
        print("✅ Dashboard page loaded successfully!")
        # Check if it contains expected dashboard content
        if "Dashboard" in response.text or "medicines" in response.text.lower() or "dashboard" in response.text.lower():
            print("✅ Dashboard content is rendered correctly!")
            sys.exit(0)
        else:
            print("⚠️  Dashboard may have loaded but content looks unusual")
            print(f"First 300 chars: {response.text[:300]}")
            sys.exit(1)
    else:
        print(f"❌ Error loading dashboard: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

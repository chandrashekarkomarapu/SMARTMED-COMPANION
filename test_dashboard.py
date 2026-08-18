#!/usr/bin/env python
"""Test dashboard endpoint after fixes."""

import httpx
import sys

def run_tests():
    client = httpx.Client()
    try:
        response = client.get("http://localhost:8000/dashboard", follow_redirects=True)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("[PASS] Dashboard page loaded successfully!")
            if "Dashboard" in response.text or "medicines" in response.text.lower() or "dashboard" in response.text.lower():
                print("[PASS] Dashboard content is rendered correctly!")
                return 0
            else:
                print("[WARN] Dashboard may have loaded but content looks unusual")
                print(f"First 300 chars: {response.text[:300]}")
                return 1
        else:
            print(f"[FAIL] Error loading dashboard: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return 1
    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

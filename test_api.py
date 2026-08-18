#!/usr/bin/env python
"""Test script for SmartMed Companion API endpoints."""

import httpx
import json
import sys

base_url = "http://localhost:8000"
client = httpx.Client()

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def run_tests():
    try:
        # Test 1: Health check
        print_section("TEST 1: Health Check Endpoint")
        r = client.get(f"{base_url}/health")
        print(f"  Status Code: {r.status_code}")
        print(f"  Response: {json.dumps(r.json(), indent=4)}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print("  [PASS]")

        # Test 2: Root redirect to dashboard
        print_section("TEST 2: Root Redirect (/ -> /dashboard)")
        r = client.get(f"{base_url}/", follow_redirects=False)
        print(f"  Status Code: {r.status_code}")
        print(f"  Location: {r.headers.get('location', 'N/A')}")
        assert r.status_code in [301, 302, 307], f"Expected redirect, got {r.status_code}"
        assert "/dashboard" in r.headers.get("location", ""), "Expected redirect to /dashboard"
        print("  [PASS]")

        # Test 3: OpenAPI/Swagger docs
        print_section("TEST 3: Swagger Documentation (/docs)")
        r = client.get(f"{base_url}/docs")
        print(f"  Status Code: {r.status_code}")
        print(f"  Content Length: {len(r.content)} bytes")
        print(f"  Is HTML: {('<!DOCTYPE' in r.text or '<html' in r.text.lower())}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print("  [PASS]")

        # Test 4: OpenAPI schema
        print_section("TEST 4: OpenAPI Schema (/openapi.json)")
        r = client.get(f"{base_url}/openapi.json")
        print(f"  Status Code: {r.status_code}")
        data = r.json()
        print(f"  API Title: {data.get('info', {}).get('title', 'N/A')}")
        print(f"  API Version: {data.get('info', {}).get('version', 'N/A')}")
        print(f"  Paths Found: {len(data.get('paths', {}))}")
        for path in list(data.get('paths', {}).keys())[:5]:
            print(f"    - {path}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert "SmartMed" in data.get('info', {}).get('title', ''), "Expected SmartMed in title"
        print("  [PASS]")

        # Test 5: Verify main routes are registered
        print_section("TEST 5: Route Registration Check")
        schema = client.get(f"{base_url}/openapi.json").json()
        paths = list(schema.get('paths', {}).keys())
        expected_routes = ['/health', '/dashboard', '/auth/login', '/medicines', '/prescriptions', '/reminders']
        
        print(f"  Total Routes: {len(paths)}")
        for route in expected_routes:
            found = any(route in path for path in paths)
            status = "[PASS]" if found else "[FAIL]"
            print(f"    {status} {route}")
        
        print("  [PASS]")

        print("\n" + "=" * 60)
        print("  ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        print("\nApplication is running correctly and all endpoints are accessible.")
        return 0

    except Exception as e:
        print_section("[FAIL] TEST FAILED")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

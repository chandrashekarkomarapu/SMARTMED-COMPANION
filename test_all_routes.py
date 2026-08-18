#!/usr/bin/env python
"""Comprehensive test for all SmartMed Companion routes after dashboard fix."""

import httpx
import sys

base_url = "http://localhost:8000"
client = httpx.Client()

test_results = []

def test_route(route_name, route_path, expected_status=200, check_content=None):
    """Test a single route."""
    try:
        response = client.get(f"{base_url}{route_path}", follow_redirects=True, timeout=10)
        status_ok = response.status_code == expected_status
        content_ok = True
        
        if check_content and response.status_code == 200:
            content_ok = check_content.lower() in response.text.lower()
        
        success = status_ok and content_ok
        test_results.append({
            "route": route_name,
            "path": route_path,
            "status": response.status_code,
            "success": success,
            "size": len(response.content)
        })
        return success
    except Exception as e:
        test_results.append({
            "route": route_name,
            "path": route_path,
            "status": "ERROR",
            "success": False,
            "error": str(e)
        })
        return False

def run_tests():
    print("=" * 70)
    print("  SmartMed Companion - Route Testing After Dashboard Fix")
    print("=" * 70)

    # Test each route
    routes_to_test = [
        ("Health Check", "/health", 200, None),
        ("Dashboard", "/dashboard", 200, "medicine"),
        ("Medicines", "/medicines", 200, "medicine"),
        ("Reminders", "/reminders", 200, "reminder"),
        ("Safety", "/safety", 200, "safety"),
        ("Emergency", "/emergency", 200, "emergency"),
        ("Scanner", "/scanner", 200, "scanner"),
    ]

    print("\nRunning tests...\n")
    for route_name, route_path, expected_status, content_check in routes_to_test:
        result = test_route(route_name, route_path, expected_status, content_check)
        status_symbol = "[PASS]" if result else "[FAIL]"
        print(f"  {status_symbol} {route_name:20} {route_path:30}")

    # Print detailed results
    print("\n" + "=" * 70)
    print("  Detailed Results:")
    print("=" * 70)

    all_passed = True
    for result in test_results:
        status = "[PASS]" if result["success"] else "[FAIL]"
        print(f"\n{status} - {result['route']}")
        print(f"   Path:   {result['path']}")
        print(f"   Status: {result.get('status', 'N/A')}")
        if "error" in result:
            print(f"   Error:  {result['error']}")
        else:
            print(f"   Size:   {result['size']} bytes")
        
        if not result["success"]:
            all_passed = False

    # Summary
    print("\n" + "=" * 70)
    passed_count = sum(1 for r in test_results if r["success"])
    total_count = len(test_results)
    print(f"  Summary: {passed_count}/{total_count} tests passed")
    print("=" * 70)

    if all_passed:
        print("\nALL TESTS PASSED\n")
        return 0
    else:
        print("\nSome tests failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

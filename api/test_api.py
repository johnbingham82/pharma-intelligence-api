#!/usr/bin/env python3
"""
API Test Suite
Tests all endpoints with real data
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_test(name):
    """Print test header"""
    print(f"\n{'='*80}")
    print(f"TEST: {name}")
    print('='*80)


def print_response(response):
    """Pretty print response"""
    print(f"\nStatus: {response.status_code}")
    print(f"Time: {response.elapsed.total_seconds():.2f}s")
    
    if response.headers.get('X-Process-Time'):
        print(f"Process Time: {float(response.headers['X-Process-Time']):.3f}s")
    
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))


def test_health():
    """Test health check endpoint"""
    print_test("Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    assert response.status_code == 200
    print("✅ PASS")


def test_root():
    """Test root endpoint"""
    print_test("Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    assert response.status_code == 200
    print("✅ PASS")


def test_countries():
    """Test countries list"""
    print_test("List Countries")
    response = requests.get(f"{BASE_URL}/countries")
    print_response(response)
    assert response.status_code == 200
    assert len(response.json()) > 0
    print("✅ PASS")


def test_drug_search():
    """Test drug search"""
    print_test("Drug Search")
    
    payload = {
        "query": "metformin",
        "country": "UK",
        "limit": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/drugs/search",
        json=payload
    )
    
    print_response(response)
    assert response.status_code == 200
    assert response.json()['count'] > 0
    print("✅ PASS")


def test_drug_lookup():
    """Test quick drug lookup"""
    print_test("Drug Lookup")
    
    response = requests.get(
        f"{BASE_URL}/drugs/lookup",
        params={"name": "metformin", "country": "UK"}
    )
    
    print_response(response)
    assert response.status_code == 200
    assert 'drug_code' in response.json()
    print("✅ PASS")


def test_analysis():
    """Test full drug analysis"""
    print_test("Drug Analysis (Metformin)")
    
    payload = {
        "company": "Generic",
        "drug_name": "metformin",
        "country": "UK",
        "top_n": 10,
        "scorer": "market_share"
    }
    
    print(f"\nRequest:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload
    )
    
    print_response(response)
    assert response.status_code == 200
    
    data = response.json()
    assert data['market_summary']['total_prescribers'] > 0
    assert len(data['top_opportunities']) > 0
    
    print(f"\n📊 Key Metrics:")
    print(f"   Prescribers: {data['market_summary']['total_prescribers']:,}")
    print(f"   Total Prescriptions: {data['market_summary']['total_prescriptions']:,}")
    print(f"   Top Opportunity: {data['top_opportunities'][0]['prescriber_name']}")
    
    print("✅ PASS")


def test_invalid_drug():
    """Test error handling for invalid drug"""
    print_test("Error Handling - Invalid Drug")
    
    payload = {
        "company": "Test",
        "drug_name": "invalid_drug_xyz_123",
        "country": "UK",
        "top_n": 10
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload
    )
    
    print_response(response)
    assert response.status_code == 404
    print("✅ PASS")


def test_invalid_country():
    """Test error handling for invalid country"""
    print_test("Error Handling - Invalid Country")
    
    payload = {
        "company": "Test",
        "drug_name": "metformin",
        "country": "ZZ",  # Invalid country
        "top_n": 10
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload
    )
    
    print_response(response)
    assert response.status_code == 400
    print("✅ PASS")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("PHARMA INTELLIGENCE API - TEST SUITE")
    print("="*80)
    print(f"\nTarget: {BASE_URL}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("List Countries", test_countries),
        ("Drug Search", test_drug_search),
        ("Drug Lookup", test_drug_lookup),
        ("Drug Analysis", test_analysis),
        ("Error: Invalid Drug", test_invalid_drug),
        ("Error: Invalid Country", test_invalid_country),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ FAIL: {e}")
            failed += 1
        except requests.exceptions.ConnectionError:
            print(f"\n❌ FAIL: Cannot connect to API. Is it running?")
            print(f"   Start server with: python api/main.py")
            failed += 1
            break
        except Exception as e:
            print(f"\n❌ FAIL: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED!")
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
    
    print()


if __name__ == "__main__":
    run_all_tests()

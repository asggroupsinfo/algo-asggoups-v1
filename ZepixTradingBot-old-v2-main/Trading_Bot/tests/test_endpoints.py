"""Test all bot endpoints"""
import requests
import json
import time

BASE_URL = "http://localhost:80"

def test_endpoint(name, url, method="GET", data=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ {name}")
            print(f"   Status: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
        else:
            print(f"❌ {name}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

print("=" * 70)
print("TESTING ZEPIX TRADING BOT ENDPOINTS")
print("=" * 70)

# Wait for server to start
print("\nWaiting for server to be ready...")
time.sleep(2)

results = []

print("\n[1/5] Testing Root Endpoint...")
results.append(test_endpoint("GET /", f"{BASE_URL}/"))

print("\n[2/5] Testing Health Endpoint...")
results.append(test_endpoint("GET /health", f"{BASE_URL}/health"))

print("\n[3/5] Testing Status Endpoint...")
results.append(test_endpoint("GET /status", f"{BASE_URL}/status"))

print("\n[4/5] Testing Config Endpoint...")
results.append(test_endpoint("GET /config", f"{BASE_URL}/config"))

print("\n[5/5] Testing Webhook Endpoint...")
test_alert = {
    "symbol": "EURUSD",
    "action": "BUY",
    "sl": "1.0500",
    "tp": "1.0600"
}
results.append(test_endpoint("POST /webhook", f"{BASE_URL}/webhook", method="POST", data=test_alert))

print("\n" + "=" * 70)
print(f"RESULTS: {sum(results)}/5 endpoints working")
print("=" * 70)

if sum(results) == 5:
    print("\n🎉 ALL ENDPOINTS WORKING! BOT IS LIVE ON PORT 80!")
else:
    print(f"\n⚠️  {5 - sum(results)} endpoint(s) failed")

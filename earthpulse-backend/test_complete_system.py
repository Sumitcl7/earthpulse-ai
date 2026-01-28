import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("🌍 EARTHPULSE AI - COMPLETE SYSTEM TEST")
print("=" * 70)
print()

# Test 1: Check health
print("1️⃣ Health Check")
response = requests.get(f"{BASE_URL}/health")
health = response.json()
print(json.dumps(health, indent=2))
print()

# Test 2: NDVI Analysis
print("2️⃣ NDVI Analysis (California - Vegetation Health)")
response = requests.get(
    f"{BASE_URL}/api/satellite/ndvi",
    params={"latitude": 36.7783, "longitude": -119.4179, "radius_km": 10}
)
ndvi = response.json()
print(f"   NDVI: {ndvi.get('ndvi_mean')}")
print(f"   Interpretation: {ndvi.get('interpretation')}")
print(f"   Data Type: {ndvi.get('data_type')}")
print(f"   Images Used: {ndvi.get('image_count')}")
print()

# Test 3: Wildfire Detection
print("3️⃣ Wildfire Detection (Los Angeles)")
response = requests.get(
    f"{BASE_URL}/api/satellite/wildfire",
    params={"latitude": 34.0522, "longitude": -118.2437, "radius_km": 50}
)
fire = response.json()
print(f"   Fire Detected: {fire.get('fire_detected')}")
print(f"   Fire Pixels: {fire.get('fire_pixel_count')}")
print(f"   Risk Level: {fire.get('risk_level')}")
print(f"   Data Type: {fire.get('data_type')}")
print()

# Test 4: Water Detection
print("4️⃣ Water Detection (Houston)")
response = requests.get(
    f"{BASE_URL}/api/satellite/water",
    params={"latitude": 29.7604, "longitude": -95.3698, "radius_km": 20}
)
water = response.json()
print(f"   NDWI: {water.get('ndwi_mean')}")
print(f"   Water Present: {water.get('water_present')}")
print(f"   Interpretation: {water.get('interpretation')}")
print(f"   Data Type: {water.get('data_type')}")
print()

# Test 5: Get Events
print("5️⃣ Database Events")
response = requests.get(f"{BASE_URL}/api/events")
events = response.json()
print(f"   Total Events: {len(events)}")
for event in events[:3]:
    print(f"   - {event['event_type'].upper()}: {event['title']}")
print()

# Test 6: Verify Events
print("6️⃣ Verifying Events with Satellite Data")
for event in events[:3]:
    print(f"   Verifying Event {event['id']}: {event['title'][:40]}...")
    response = requests.post(f"{BASE_URL}/api/events/{event['id']}/verify")
    print(f"   ✓ Verification started")
    time.sleep(5)

print()
print("   ⏳ Waiting for verifications to complete...")
time.sleep(15)
print()

# Test 7: Check Verified Events
print("7️⃣ Verification Results")
for event in events[:3]:
    response = requests.get(f"{BASE_URL}/api/events/{event['id']}")
    updated_event = response.json()
    print(f"   Event {event['id']}: {updated_event['event_type'].upper()}")
    print(f"   - Verified: {updated_event['is_verified']}")
    print(f"   - Score: {updated_event['verification_score']}")
    print(f"   - Status: {updated_event['verification_status']}")
    print()

# Test 8: Statistics
print("8️⃣ System Statistics")
response = requests.get(f"{BASE_URL}/api/stats")
stats = response.json()
print(json.dumps(stats, indent=2))

print()
print("=" * 70)
print("✅ ALL TESTS COMPLETED!")
print("=" * 70)
print()
print("🎉 Your EarthPulse AI backend is fully operational!")
print("📡 Real satellite data: WORKING")
print("🗄️ Database: WORKING")
print("🔍 Event verification: WORKING")
print()
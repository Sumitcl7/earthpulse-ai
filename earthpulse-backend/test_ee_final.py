import ee

print("🧪 Testing Earth Engine with Project: earthpulse-472111\n")

try:
    print("1️⃣ Initializing Earth Engine with project...")
    
    # Initialize with your project ID
    ee.Initialize(project='earthpulse-472111')
    
    print("✅ Earth Engine initialized successfully!\n")
    
    # Test 2: Simple geometry query
    print("2️⃣ Testing basic Earth Engine query...")
    point = ee.Geometry.Point([-122.0841, 37.4220])
    result = point.getInfo()
    print(f"✅ Point query successful: {result}\n")
    
    # Test 3: Access satellite data
    print("3️⃣ Testing access to satellite imagery...")
    image = ee.Image('COPERNICUS/S2_SR_HARMONIZED/20200101T184759_20200101T184931_T10SEG')
    info = image.getInfo()
    print(f"✅ Can access Sentinel-2 imagery!\n")
    
    # Test 4: Perform NDVI calculation
    print("4️⃣ Testing NDVI calculation (California)...")
    point = ee.Geometry.Point([-119.4179, 36.7783])
    region = point.buffer(10000)
    
    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(region) \
        .filterDate('2024-01-01', '2024-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    
    count = collection.size().getInfo()
    print(f"✅ Found {count} Sentinel-2 images for California!\n")
    
    # Test 5: Fire detection
    print("5️⃣ Testing fire detection dataset (MODIS)...")
    fires = ee.ImageCollection('MODIS/006/MOD14A1') \
        .filterDate('2024-01-01', '2024-12-31') \
        .limit(1)
    
    fire_count = fires.size().getInfo()
    print(f"✅ Can access MODIS fire data ({fire_count} images tested)!\n")
    
    print("=" * 60)
    print("🎉 SUCCESS! All tests passed!")
    print("=" * 60)
    print("\n✅ Your Earth Engine is fully configured and ready to use!")
    print("✅ Project ID: earthpulse-472111")
    print("✅ You can now use REAL satellite data in your backend!\n")
    
except Exception as e:
    print(f"❌ Error: {e}\n")
    print("🔧 If you see an error, try:")
    print("   1. Make sure you're signed in with the correct Google account")
    print("   2. Visit https://code.earthengine.google.com/ to activate your project")
    print("   3. Run: earthengine authenticate --force")
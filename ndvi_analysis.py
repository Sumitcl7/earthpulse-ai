import ee
import geemap
import folium
import matplotlib.pyplot as plt

# Initialize Earth Engine
ee.Initialize(project="earthpulse-472111")

# Define Area of Interest (AOI)
aoi = ee.Geometry.Polygon([
    [
        [76.84, 12.56],
        [77.86, 12.56],
        [77.86, 13.55],
        [76.84, 13.55],
        [76.84, 12.56]
    ]
])

# Load Sentinel-2 data and filter
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(aoi)
    .filterDate("2024-01-01", "2024-12-31")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
)

# Take median image
image = collection.median()

# Compute NDVI
ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

# Create a map
Map = folium.Map(location=[12.9, 77.5], zoom_start=8)
Map = geemap.Map(center=[12.9, 77.5], zoom=8)

# Add NDVI layer
ndvi_vis = {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}
Map.addLayer(ndvi, ndvi_vis, "NDVI")
Map.addLayer(aoi, {}, "AOI")

# Save interactive HTML map
Map.to_html("ndvi_map.html")
print("✅ NDVI map saved as ndvi_map.html")

# --- Export full-resolution GeoTIFF to Google Drive ---
task = ee.batch.Export.image.toDrive(
    image=ndvi,
    description="NDVI_FullResolution",
    folder="EarthEngine",
    fileNamePrefix="NDVI_Full",
    region=aoi,
    scale=10,
    crs="EPSG:4326"
)
task.start()
print("✅ NDVI GeoTIFF export started (check your Google Drive > EarthEngine folder)")

# --- Save a low-resolution preview locally ---
geemap.ee_export_image(
    ndvi,
    filename="NDVI_preview.tif",
    scale=100,  # lower resolution so it downloads fast
    region=aoi
)
print("✅ Low-resolution NDVI preview saved locally as NDVI_preview.tif")

# --- Compute NDVI stats ---
stats = ndvi.reduceRegion(
    reducer=ee.Reducer.mean().combine(
        reducer2=ee.Reducer.minMax(), sharedInputs=True
    ),
    geometry=aoi,
    scale=30,
    maxPixels=1e9
).getInfo()

print("📊 NDVI Stats:", stats)

# --- Plot histogram ---
hist = ndvi.reduceRegion(
    reducer=ee.Reducer.histogram(255),
    geometry=aoi,
    scale=30,
    maxPixels=1e9
).getInfo()

plt.figure(figsize=(8, 5))
plt.bar(hist["NDVI"]["bucketMeans"], hist["NDVI"]["histogram"], width=0.05, color="green")
plt.title("NDVI Histogram")
plt.xlabel("NDVI Value")
plt.ylabel("Pixel Count")
plt.savefig("ndvi_histogram.png")
plt.close()

print("✅ NDVI histogram saved as ndvi_histogram.png")

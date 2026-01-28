# 🛰️ EarthPulse AI – Satellite APIs

## 1. Google Earth Engine (GEE)

**What Data:** NDVI (vegetation), water index, soil, land cover, flood & wildfire detection  
**Use Cases:** Wildfires, Floods, Deforestation

**Step-by-Step Setup (Beginner Friendly):**

1. Sign up: [https://signup.earthengine.google.com](https://signup.earthengine.google.com)

   - Use your Google account.
   - Fill in the form (Institution: “Personal Project” or “Student”).
   - Approval may take a few hours to a day.

2. Open the Code Editor: [https://code.earthengine.google.com](https://code.earthengine.google.com)

   - This is a browser IDE; you can run JavaScript scripts directly here.

3. Try a Simple NDVI Script:

```javascript
// Load Sentinel-2 imagery
var dataset = ee
  .ImageCollection("COPERNICUS/S2")
  .filterDate("2023-05-01", "2023-05-10")
  .filterBounds(ee.Geometry.Point([77.5946, 12.9716])); // Bengaluru

// Median composite
var image = dataset.median();

// Compute NDVI
var ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI");

// Visualization
Map.centerObject(dataset, 9);
Map.addLayer(ndvi, { min: 0, max: 1, palette: ["white", "green"] }, "NDVI");
```

# 🛰️ Satellite APIs for EarthPulse AI

## 1. Google Earth Engine (GEE)

- **Data:** NDVI, water index, soil, land cover, flood, drought, deforestation, wildfire mapping.
- **Use Cases:**
  - Wildfires → thermal anomalies
  - Floods → pre/post water index comparison
  - Deforestation → vegetation loss using NDVI
- **Authentication:**
  - Sign up at [Google Earth Engine](https://earthengine.google.com/)
  - Use Code Editor (JavaScript) or Python API (`earthengine-api`)
  - Authenticate via: `earthengine authenticate`

## 2. Sentinel Hub API

- **Data:** Sentinel-1 (radar), Sentinel-2 (optical, vegetation), Sentinel-3 (ocean/atmosphere)
- **Use Cases:**
  - Flood detection (Sentinel-1 SAR)
  - Deforestation (Sentinel-2 NDVI)
  - Air pollution / heat anomalies (Sentinel-3)
- **Authentication:**
  - Register at [Sentinel Hub](https://www.sentinel-hub.com/)
  - Create OAuth client → get `client_id` + `client_secret`
  - Use Python SDK `sentinelhub-py`

## 3. NASA EarthData / MODIS

- **Data:** Thermal anomalies, fire hotspots, snow, floods; daily global coverage
- **Use Cases:**
  - Wildfires → hotspots
  - Flood mapping
  - Snow cover & drought
- **Authentication:**
  - Register at [NASA EarthData](https://earthdata.nasa.gov/)
  - Access datasets via LAADS DAAC
  - Python: `pip install earthaccess` → `earthaccess.login(strategy="netrc")`

## 4. USGS Landsat

- **Data:** 30m optical resolution since 1972
- **Use Cases:**
  - Deforestation trends
  - Urban growth
  - Glacier retreat / desertification
- **Authentication:**
  - Create account at [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
  - Download manually or via API
  - Python: `pip install landsatxplore` → login via `API("username","password")`

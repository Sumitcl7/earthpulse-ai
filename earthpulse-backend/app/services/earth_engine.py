# app/services/earth_engine.py
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Your Earth Engine Project ID
EE_PROJECT_ID = 'earthpulse-472111'

# Try to import and initialize real Earth Engine
USE_REAL_EE = False

try:
    import ee
    
    try:
        # Initialize Earth Engine with your project ID
        ee.Initialize(project=EE_PROJECT_ID)
        USE_REAL_EE = True
        logger.info(f"✅ Real Earth Engine initialized with project: {EE_PROJECT_ID}")
    except Exception as e:
        logger.warning(f"⚠️ Earth Engine initialization failed: {e}")
        logger.info("🔄 Falling back to Mock Earth Engine")
        USE_REAL_EE = False
        
except ImportError:
    logger.warning("⚠️ earthengine-api not installed")
    logger.info("🔄 Using Mock Earth Engine")
    USE_REAL_EE = False


# =============================================================================
# REAL EARTH ENGINE SERVICE
# =============================================================================

if USE_REAL_EE:
    logger.info("📡 Using Real Google Earth Engine with LIVE satellite data")
    
    class EarthEngineService:
        """Real Google Earth Engine service using live satellite data"""
        
        def __init__(self):
            self.initialized = True
            self.project_id = EE_PROJECT_ID
            logger.info("🛰️ Real Earth Engine Service ready")
        
        def get_ndvi(self, latitude: float, longitude: float, 
                     start_date: str = None, end_date: str = None,
                     radius_km: float = 10) -> Dict:
            """
            Calculate NDVI (Normalized Difference Vegetation Index) using real Sentinel-2 data
            
            NDVI values range from -1 to 1:
            - High values (0.6-0.9): Dense, healthy vegetation
            - Medium values (0.2-0.5): Sparse vegetation, grasslands
            - Low values (<0.2): Barren land, urban areas
            - Negative values: Water bodies
            """
            try:
                # Set default date range if not provided
                if not end_date:
                    end_date = datetime.now().strftime('%Y-%m-%d')
                if not start_date:
                    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                
                logger.info(f"🌿 NDVI analysis for ({latitude}, {longitude}) | {start_date} to {end_date}")
                
                # Create point and buffer region
                point = ee.Geometry.Point([longitude, latitude])
                region = point.buffer(radius_km * 1000)  # Convert km to meters
                
                # Get Sentinel-2 Surface Reflectance imagery
                collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                    .filterBounds(region) \
                    .filterDate(start_date, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                
                # Calculate NDVI for each image
                def add_ndvi(image):
                    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
                    return image.addBands(ndvi)
                
                collection_with_ndvi = collection.map(add_ndvi)
                
                # Get mean NDVI across all images
                mean_ndvi = collection_with_ndvi.select('NDVI').mean()
                
                # Calculate statistics
                stats = mean_ndvi.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=region,
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                # Get metadata
                image_count = collection.size().getInfo()
                ndvi_value = stats.get('NDVI', None)
                
                if ndvi_value is not None:
                    logger.info(f"✅ NDVI: {ndvi_value:.3f} | Images used: {image_count}")
                else:
                    logger.warning(f"⚠️ No NDVI data available | Images found: {image_count}")
                
                return {
                    "ndvi_mean": round(ndvi_value, 3) if ndvi_value is not None else None,
                    "location": {
                        "latitude": latitude, 
                        "longitude": longitude,
                        "radius_km": radius_km
                    },
                    "date_range": {"start": start_date, "end": end_date},
                    "image_count": image_count,
                    "analysis_type": "vegetation_health",
                    "interpretation": self._interpret_ndvi(ndvi_value),
                    "satellite_source": "Sentinel-2 SR",
                    "data_type": "real",
                    "project": self.project_id
                }
                
            except Exception as e:
                logger.error(f"❌ Error calculating NDVI: {e}")
                return {
                    "error": str(e), 
                    "location": {"latitude": latitude, "longitude": longitude},
                    "analysis_type": "vegetation_health"
                }
        
        def detect_wildfires(self, latitude: float, longitude: float,
                            start_date: str = None, end_date: str = None,
                            radius_km: float = 50) -> Dict:
            """
            Detect wildfires using real MODIS thermal anomaly data
            
            Uses NASA's MODIS Active Fire product which detects thermal anomalies
            indicating active fires or recently burned areas.
            """
            try:
                # Set default date range
                if not end_date:
                    end_date = datetime.now().strftime('%Y-%m-%d')
                if not start_date:
                    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                
                logger.info(f"🔥 Fire detection for ({latitude}, {longitude}) | {start_date} to {end_date}")
                
                # Create point and buffer region
                point = ee.Geometry.Point([longitude, latitude])
                region = point.buffer(radius_km * 1000)
                
                # Get MODIS fire data
                fires = ee.ImageCollection('MODIS/006/MOD14A1') \
                    .filterBounds(region) \
                    .filterDate(start_date, end_date)
                
                # Get maximum fire mask (any fire detected in the period)
                fire_mask = fires.select('FireMask').max()
                
                # Calculate fire statistics
                fire_stats = fire_mask.reduceRegion(
                    reducer=ee.Reducer.sum(),
                    geometry=region,
                    scale=1000,
                    maxPixels=1e9
                ).getInfo()
                
                fire_count = int(fire_stats.get('FireMask', 0))
                
                if fire_count > 0:
                    logger.warning(f"🔥 Fire detected! {fire_count} fire pixels found")
                else:
                    logger.info(f"✅ No fires detected in the area")
                
                return {
                    "fire_detected": fire_count > 0,
                    "fire_pixel_count": fire_count,
                    "estimated_area_km2": round(fire_count * 1.0, 2),  # Each pixel ~1km²
                    "location": {
                        "latitude": latitude, 
                        "longitude": longitude,
                        "radius_km": radius_km
                    },
                    "date_range": {"start": start_date, "end": end_date},
                    "risk_level": self._assess_fire_risk(fire_count),
                    "analysis_type": "wildfire_detection",
                    "satellite_source": "MODIS Active Fire",
                    "resolution": "1km",
                    "data_type": "real",
                    "project": self.project_id
                }
                
            except Exception as e:
                logger.error(f"❌ Error detecting wildfires: {e}")
                return {
                    "error": str(e), 
                    "location": {"latitude": latitude, "longitude": longitude},
                    "analysis_type": "wildfire_detection"
                }
        
        def detect_water_changes(self, latitude: float, longitude: float,
                                start_date: str = None, end_date: str = None,
                                radius_km: float = 20) -> Dict:
            """
            Detect water changes using real Sentinel-2 NDWI (Normalized Difference Water Index)
            
            NDWI values:
            - > 0.3: Water bodies, potential flooding
            - 0 to 0.3: Moderate moisture, wetlands
            - < 0: Dry land, potential drought
            """
            try:
                # Set default date range
                if not end_date:
                    end_date = datetime.now().strftime('%Y-%m-%d')
                if not start_date:
                    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                
                logger.info(f"💧 Water detection for ({latitude}, {longitude}) | {start_date} to {end_date}")
                
                # Create point and buffer region
                point = ee.Geometry.Point([longitude, latitude])
                region = point.buffer(radius_km * 1000)
                
                # Get Sentinel-2 imagery
                collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                    .filterBounds(region) \
                    .filterDate(start_date, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                
                # Calculate NDWI for each image
                def add_ndwi(image):
                    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
                    return image.addBands(ndwi)
                
                collection_with_ndwi = collection.map(add_ndwi)
                
                # Get mean NDWI
                mean_ndwi = collection_with_ndwi.select('NDWI').mean()
                
                # Calculate statistics
                stats = mean_ndwi.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=region,
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                ndwi_value = stats.get('NDWI', None)
                image_count = collection.size().getInfo()
                
                if ndwi_value is not None:
                    if ndwi_value > 0.3:
                        logger.warning(f"💧 High water content detected: NDWI = {ndwi_value:.3f}")
                    else:
                        logger.info(f"✅ NDWI: {ndwi_value:.3f} | Images used: {image_count}")
                else:
                    logger.warning(f"⚠️ No NDWI data available | Images found: {image_count}")
                
                return {
                    "ndwi_mean": round(ndwi_value, 3) if ndwi_value is not None else None,
                    "water_present": ndwi_value > 0.3 if ndwi_value is not None else False,
                    "location": {
                        "latitude": latitude, 
                        "longitude": longitude,
                        "radius_km": radius_km
                    },
                    "date_range": {"start": start_date, "end": end_date},
                    "image_count": image_count,
                    "interpretation": self._interpret_ndwi(ndwi_value),
                    "analysis_type": "water_detection",
                    "satellite_source": "Sentinel-2 SR",
                    "data_type": "real",
                    "project": self.project_id
                }
                
            except Exception as e:
                logger.error(f"❌ Error detecting water changes: {e}")
                return {
                    "error": str(e), 
                    "location": {"latitude": latitude, "longitude": longitude},
                    "analysis_type": "water_detection"
                }
        
        def get_satellite_image_url(self, latitude: float, longitude: float,
                                   date: str = None, zoom: int = 12) -> Optional[str]:
            """
            Get a visual RGB satellite image URL
            """
            try:
                if not date:
                    date = datetime.now().strftime('%Y-%m-%d')
                
                point = ee.Geometry.Point([longitude, latitude])
                
                # Get Sentinel-2 image
                image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                    .filterBounds(point) \
                    .filterDate(date, (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')) \
                    .sort('CLOUDY_PIXEL_PERCENTAGE') \
                    .first()
                
                # Get thumbnail URL (RGB visualization)
                url = image.getThumbURL({
                    'min': 0,
                    'max': 3000,
                    'bands': ['B4', 'B3', 'B2'],  # RGB
                    'dimensions': 512,
                    'region': point.buffer(5000).bounds()
                })
                
                return url
                
            except Exception as e:
                logger.error(f"Error getting satellite image: {e}")
                return None
        
        @staticmethod
        def _interpret_ndvi(ndvi: float) -> str:
            """Interpret NDVI value"""
            if ndvi is None:
                return "No data available - check date range or cloud coverage"
            elif ndvi < -0.1:
                return "Water bodies"
            elif ndvi < 0:
                return "Clouds or snow"
            elif ndvi < 0.2:
                return "Barren land, rock, sand, or urban areas"
            elif ndvi < 0.35:
                return "Sparse vegetation, shrubland, or grassland"
            elif ndvi < 0.5:
                return "Moderate vegetation, agricultural land"
            elif ndvi < 0.7:
                return "Dense vegetation, healthy forests"
            else:
                return "Very dense, healthy vegetation - tropical rainforests"
        
        @staticmethod
        def _assess_fire_risk(fire_count: int) -> str:
            """Assess fire risk level based on detected fire pixels"""
            if fire_count == 0:
                return "low"
            elif fire_count < 5:
                return "medium"
            elif fire_count < 15:
                return "high"
            else:
                return "critical"
        
        @staticmethod
        def _interpret_ndwi(ndwi: float) -> str:
            """Interpret NDWI value"""
            if ndwi is None:
                return "No data available - check date range or cloud coverage"
            elif ndwi > 0.5:
                return "High water content - large water bodies or significant flooding"
            elif ndwi > 0.3:
                return "Moderate water content - potential flooding or wetlands"
            elif ndwi > 0.1:
                return "Low water content - moist soil or vegetation"
            elif ndwi > -0.1:
                return "Minimal water content - dry soil"
            else:
                return "Very low water content - barren land, potential drought conditions"
    
    # Create singleton instance
    earth_engine_service = EarthEngineService()


# =============================================================================
# FALLBACK TO MOCK EARTH ENGINE IF REAL EE FAILED
# =============================================================================

else:
    logger.info("🎭 Using Mock Earth Engine (for testing)")
    
    # Import mock service
    try:
        from .earth_engine_mock import earth_engine_service
        logger.info("✅ Mock Earth Engine Service loaded")
    except ImportError:
        logger.error("❌ Could not load Mock Earth Engine Service")
        logger.error("Please ensure earth_engine_mock.py exists in app/services/")
        
        # Create a minimal fallback
        class MinimalMockService:
            def __init__(self):
                self.initialized = False
            
            def get_ndvi(self, *args, **kwargs):
                return {"error": "Earth Engine not available"}
            
            def detect_wildfires(self, *args, **kwargs):
                return {"error": "Earth Engine not available"}
            
            def detect_water_changes(self, *args, **kwargs):
                return {"error": "Earth Engine not available"}
        
        earth_engine_service = MinimalMockService()
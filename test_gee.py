import ee

ee.Initialize(project='earthpulse-472111')  # replace with your Project ID

point = ee.Geometry.Point([77.5946, 12.9716])
image = ee.ImageCollection('COPERNICUS/S2') \
    .filterBounds(point) \
    .filterDate('2023-01-01', '2023-12-31') \
    .sort('CLOUDY_PIXEL_PERCENTAGE') \
    .first()

ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
print(ndvi.getInfo())

# OBIA Shadow-Based Building Height Estimation

This project is a **streamlit-based GUI** for estimating building heights using shadow lengths extracted from classified satellite imagery.

## Overview

This tool performs the following:
1. **Upload** a classified GeoJSON file (from OBIA segmentation/classification).
2. **Extract** shadow-building pairs using sun azimuth & elevation metadata.
3. **Estimate building heights** based on shadow lengths.
4. **Visualize** results as:
   - Interactive **map**
   - Color-coded **height plot**
   - Downloadable **GeoJSON** and **table**

## Input Requirements

- **GeoJSON** file with segmented objects including:
  - `classification` column with values: `'buildings'`, `'shadow'`
  - `geometry` column with valid polygons (in WGS84 - EPSG:4326)

- **Sun metadata**: Sun azimuth and elevation (in degrees)

- (Optional) A **.tif** image for overlay on the map.

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

3. Use the GUI to upload your Geojson file that results from OBIA classification, and then the program will calculate the buildings' length based on the sun azimuth and elevation angles.

## Output

- Map with colored building heights
- Downloadable `estimated_heights.geojson`
- Histogram and height table

##  Internals

- Reprojects geometries to UTM for accurate metric distance
- Projects sun ray from building centroid using azimuth angle
- Computes shadow intersection and estimates height using:  
  `height = shadow_length * tan(sun_elevation)`

## Dependencies

- geopandas
- shapely
- rasterio (optional)
- numpy
- matplotlib
- streamlit
- folium
- streamlit-folium

---

Developed for easy validation of OBIA-based shadow height estimation with a friendly interface.

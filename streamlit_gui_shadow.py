import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from shapely.geometry import LineString
import numpy as np
import os

def reproject_to_utm(gdf):
    centroid = gdf.unary_union.centroid
    utm_zone = int((centroid.x + 180) / 6) + 1
    return gdf.to_crs(f"EPSG:{32600 + utm_zone}")

def project_sun_line(centroid, azimuth_deg, length=100):
    azimuth_rad = np.radians(azimuth_deg)
    dx = length * np.sin(azimuth_rad)
    dy = length * np.cos(azimuth_rad)
    return LineString([centroid, (centroid.x + dx, centroid.y + dy)])

def estimate_heights(buildings_utm, shadows_utm, sun_azimuth_deg, sun_elevation_deg):
    shadow_lengths = []
    for idx, building in buildings_utm.iterrows():
        centroid = building.geometry.centroid
        sun_line = project_sun_line(centroid, sun_azimuth_deg, length=100)
        for _, shadow in shadows_utm.iterrows():
            if sun_line.intersects(shadow.geometry):
                intersection = sun_line.intersection(shadow.geometry)
                if intersection.is_empty:
                    continue
                try:
                    length = centroid.distance(intersection)
                    shadow_lengths.append(length)
                    break
                except:
                    shadow_lengths.append(np.nan)
                    break
        else:
            shadow_lengths.append(np.nan)
    sun_elevation_rad = np.radians(sun_elevation_deg)
    heights = [s * np.tan(sun_elevation_rad) if not np.isnan(s) else np.nan for s in shadow_lengths]
    buildings_utm["shadow_length_m"] = shadow_lengths
    buildings_utm["estimated_height_m"] = heights
    return buildings_utm

# Streamlit GUI
st.set_page_config(layout="wide")
st.title("Building Height Estimation from Shadows")

uploaded_geojson = st.file_uploader("Upload Classified OBIA GeoJSON", type=["geojson"])
sun_azimuth = st.number_input("Sun Azimuth Angle (degrees)", value=144.5)
sun_elevation = st.number_input("Sun Elevation Angle (degrees)", value=34.2)

if uploaded_geojson:
    gdf = gpd.read_file(uploaded_geojson)
    buildings = gdf[gdf["classification"] == "buildings"].copy()
    shadows = gdf[gdf["classification"] == "shadow"].copy()

    buildings_utm = reproject_to_utm(buildings)
    shadows_utm = reproject_to_utm(shadows)

    result = estimate_heights(buildings_utm, shadows_utm, sun_azimuth, sun_elevation)
    result_wgs = result.to_crs("EPSG:4326")

    st.success("✅ Height estimation complete")
    st.write("### Estimated Heights Table")
    st.dataframe(result_wgs[["segment_id", "shadow_length_m", "estimated_height_m"]])

    st.download_button(
        label="Download as GeoJSON",
        data=result_wgs.to_json(),
        file_name="estimated_heights.geojson",
        mime="application/geo+json"
    )

    st.write("### Map of Estimated Heights")
    center = [result_wgs.geometry.centroid.y.mean(), result_wgs.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=18)
    folium.GeoJson(result_wgs).add_to(m)
    folium_static(m)

# 🏙️ Estimation of Building Height using shadow length and OBIA from Satellite Imagery

## Overview
This project estimates **building heights** from high-resolution panchromatic imagery using a combination of:

- **Object-Based Image Analysis (OBIA)** segmentation  
- **Random Forest (RF)** classification  
- **Shadow geometry** for height estimation  
- **Streamlit GUI** for a no-code user experience  

The pipeline processes imagery, identifies buildings and shadows, measures shadow lengths, and calculates heights based on solar geometry.  
Outputs can be visualized on an interactive map and exported for GIS software.

---

##  Workflow

### 1. OBIA Segmentation
- **Tool:** [`nickyspatial`]([https://github.com/NickysTeam/nickyspatial](https://github.com/kshitijrajsharma/nickyspatial/tree/master))  
- **Goal:** Split the image into homogeneous objects.  
- **Key parameters:** scale, compactness.  
- **Output:** Segmented vector layer.

*Example segmentation:*  

![Segmentation Example](https://github.com/user-attachments/assets/cf71de1a-144a-431c-a871-cd18570750e9)

---

### 2. Random Forest Classification
- **Algorithm:** `RandomForest` 
- **Classes:**  
  - `buildings`  
  - `shadow`  
  - `non_buildings`
  - `non_shadow`
- **Features:** mean & std dev of pixel values, shape metrics, area.  
- **Output:** `classified_RF.geojson`

*Example classification:*  

![Classification Example](https://github.com/user-attachments/assets/840e1fbc-0088-41bc-ac40-c8557a5a8a21)

---

### 3. Building Height Estimation
Steps:
1. Extract **buildings** and **shadows** from classification.
2. Reproject to **UTM CRS** (metric units).
3. For each building centroid:
   - Project a line using **solar azimuth**.
   - Find nearest intersecting shadow.
   - Measure shadow length in meters.
4. Convert to height: `Height = Shadow_Length × tan(Solar_Elevation)`



*Example map of estimated heights:*

The orange color represents the estimated building height based on the length of the shadow, which is indicated in gray.

![Building Height Map](https://github.com/user-attachments/assets/e746f1c7-eeb4-4c30-924a-e9ec507fd979)

#### and this image below is for estimating heights with projected shadow lines

![Estimated Heights with Projected Shadow Lines](https://github.com/user-attachments/assets/3ddd5a6b-ab0f-42ea-a595-519d7c381e24)


---

## Outputs

### Data Table Example snapshot
| segment_id | shadow_length_m | estimated_height_m |
|------------|-----------------|--------------------|
| 48         | 29.27           | 19.89              |
| 49         | 41.56           | 28.25              |
| ...        | ...             | ...                |

### Histograms
![Height Histogram](https://github.com/user-attachments/assets/d2a2e6ec-8a42-4508-aa83-d965c5a9c601)

### GeoJSON/Shapefile  
- `classified_RF.geojson` and `estimated_heights` files.

---

## Streamlit GUI

The GUI provides:
1. **Upload** a classified `.geojson` file.
2. **Input** solar azimuth & elevation.
3. **Run** estimation with one click.
4. **Visualize**:
  - Interactive map with heights
  - Data table
5. **Download** results for GIS.

*Example GUI screenshot:*  
![GUI Screenshot](https://github.com/user-attachments/assets/9291fa95-15f0-4283-b010-2d44bcdd6dc0)
![GUI image 2](https://github.com/user-attachments/assets/273360e6-87e7-4e92-b28e-3792c689326e)

---

## Installation
```bash
# Clone repository
git clone https://github.com/SaharAbdulallim/IP_Application-Development-Earth-Observation-.git
cd building-height-estimation

# Install dependencies
pip install -r requirements.txt
```

## 📄 requirements.txt

```txt
geopandas
shapely
pyproj
numpy
pandas
matplotlib
scikit-learn
nickyspatial
streamlit
streamlit-folium
folium
rasterio
````

## Usage
#### You can download and run the notebook directly on your local PC or Colab and customize it based on your goal.

## Run GUI
#### You can download the python file `streamlit_gui_shadow.py` and use this command  `streamlit run streamlit_gui_shadow.py` to run the GUI

## Limitations:
  - Requires accurate classification of shadows & buildings.
  - Dependent on correct solar geometry.
  - Terrain slopes can distort measurements.

## Future Improvements
  - Automatic extraction of sun angles from metadata.
  - Orthorectification for terrain correction.
  - Multi-date building height change analysis.
  
  







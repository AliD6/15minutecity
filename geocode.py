import pandas as pd
import requests
import geopandas as gpd
from shapely.geometry import Point

# 1. Load the data
data = pd.read_excel('15minutecity.xlsx', header=[0, 1, 2])
search_col = data.columns[11]

# 2. Flatten MultiIndex Headers
# Shapefiles do not support MultiIndex (3-level) headers.
# We must flatten them into single strings (e.g., "Level0_Level1_Level2")
data.columns = ['_'.join(str(level) for level in col).strip() for col in data.columns]
search_col_flat = data.columns[11]

headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjEwODAzN2I5NTUxZmM4YTc4OGUzODlmNTRhNGIwYmRkN2FjZTExMjJhNWQ1MjlhNGMxZWYzZTVmNzNjMGY4MGQwNjcxMjQxZjAyMGIzNDMxIn0.eyJhdWQiOiIxNTkyNiIsImp0aSI6IjEwODAzN2I5NTUxZmM4YTc4OGUzODlmNTRhNGIwYmRkN2FjZTExMjJhNWQ1MjlhNGMxZWYzZTVmNzNjMGY4MGQwNjcxMjQxZjAyMGIzNDMxIiwiaWF0IjoxNjM1NDIwNjkzLCJuYmYiOjE2MzU0MjA2OTMsImV4cCI6MTYzNzkyNjI5Mywic3ViIjoiIiwic2NvcGVzIjpbImJhc2ljIl19.eSknkj0_1s1QAMWNbAW_CG1pfaJ0vJJe2V1JTnhn5L2BvQMT-YEnKLGOhfAyvWO8L5RRkRape90lrR2JiuUoTDYD0OtUGwR56hDCoVxcvocTV7lixWQRydvxROegYMlLejkeBSBdet6U21sy-AKIiWx65fB1gY8my0FKRkQBzKlY22KhmoBSsiNAs5p8E-63bMLJUr4MFroaaHSz3RkJvsgmFVyTf9ghpjjXIgEXo-F47zEBYaA25TASw2_ef0wTqbVMdSOodnkT4X2aYlFw3M5T1hs4JDVzKA_We2ObXnhohM7SCIcB3aACImTboOdeEn9PTaPEIkhW-kYo_o6VRw'
}


def get_point(text):
    if pd.isna(text) or str(text).strip() == "":
        return None

    url = f"https://map.ir/search/v2?text={text}&$select=neighborhood&$filter=province eq تهران"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get('value'):
                coords = res_data['value'][0]['geom']['coordinates']
                # coords is [longitude, latitude]
                return Point(coords[0], coords[1])
        return None
    except:
        return None


# 3. Create the Geometry column
print("Fetching coordinates and creating points...")
data['geometry'] = data[search_col_flat].apply(get_point)

# 4. Convert to GeoDataFrame
# We filter out rows where no geometry was found to avoid errors
gdf = gpd.GeoDataFrame(data[data['geometry'].notnull()], geometry='geometry')

# 5. Set Coordinate Reference System (CRS)
# WGS84 (lat/lon) is standard for GPS coordinates
gdf.set_crs(epsg=4326, inplace=True)

# 6. Save to Shapefile
# Note: Shapefile column names are limited to 10 characters.
# GeoPandas handles this, but names might get truncated.
gdf.to_file("15min_city_results.shp", driver='ESRI Shapefile', encoding='utf-8')

print("Shapefile created successfully!")
import osmnx as ox
import networkx as nx
import numpy as np
import geopandas as gpd
import logging


logging.basicConfig(
    filename="output.log",           # Output log file
    filemode="w",                    # Overwrite file each run (use "a" to append)
    level=logging.INFO,              # Choose detail level (DEBUG, INFO, WARNING, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format with timestamp
)

# load regions
shapefile_path = "regions/mahale.shp"
regions = gpd.read_file(shapefile_path)
number_of_regions = len(regions)
logging.info(f"Regions loaded: {number_of_regions} regions found.")

regions["lon"] = regions.geometry.x
regions["lat"] = regions.geometry.y

# describe places and load places
place_name = "Tehran, Iran"
tags = {"amenity": ["hospital", "school", "pharmacy"], "leisure": "park"}
data = ox.features_from_place(place_name, tags)
logging.info("POIs received!")

data["geometry_point"] = data.geometry.apply(
    lambda geom: geom if geom.geom_type == "Point" else geom.representative_point()
)
data["lon"] = data.geometry_point.x
data["lat"] = data.geometry_point.y
data = data.set_geometry("geometry_point")
data = data[["geometry", "geometry_point", "amenity", "name", "leisure", "lat", "lon"]]

# filter places in variables
hospital = data[data["amenity"] == "hospital"]
school = data[data["amenity"] == "school"]
pharmacy = data[data["amenity"] == "pharmacy"]
park = data[data["leisure"] == "park"]
logging.info("places seperated!")

# define categories and their weights
category_weights = {
    "hospital": 1.0,
    "park": 1,
    "school": 1.0,
    "pharmacy": 4.5
}
# lists of coordinates for each category
places = {
    "hospital": list(zip(hospital["lat"], hospital["lon"])),
    "park": list(zip(park["lat"], park["lon"])),
    "school": list(zip(school["lat"], school["lon"])),
    "pharmacy": list(zip(pharmacy["lat"], pharmacy["lon"]))
}

def count_points_within_distance(G, source_node, target_coords):
    """
    Returns the number of nodes reachable from source_node with shortest path length
    less than or equal to threshold.
    """
    target_nodes = ox.distance.nearest_nodes(G,
                                             X=[lon for _, lon in target_coords],
                                             Y=[lat for lat, _ in target_coords])
    count_of_places = 0
    unique_nodes = np.unique(target_nodes)
    for tnode in unique_nodes:
        try:
            dist = nx.shortest_path_length(G, source_node, tnode, weight='length')
            if dist <= distance_threshold:
                count_of_places += 1
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
    return count_of_places


# Define walking parameters
walking_speed_m_per_min = 80  # meters per minute
distance_threshold = 15 * walking_speed_m_per_min  # 15-minute walk (1200 m)

scores = []
for idx, row in regions.iterrows():
    reference_point = (row["lat"], row["lon"])

    # Load road network in the 2Km radiused bbox of reference point
    G = ox.graph_from_point(reference_point, dist=2000, network_type='walk')
    logging.info(f"Road Network loaded! for region: {row['NAME_MAHAL']}")

    # nearest node of reference point from G as the accessible reference point
    reference_node = ox.distance.nearest_nodes(G, reference_point[1], reference_point[0])

    # Compute accessibility counts for each category
    accessibility_counts = {}
    for category, coords in places.items():
        count = count_points_within_distance(G, reference_node, coords)
        accessibility_counts[category] = count

    # Compute weighted accessibility score weighted by count * category weight
    weighted_score = sum(
        category_weights[cat] * count
        for cat, count in accessibility_counts.items()
    )

    # Output counts and weighted score
    logging.info(f"Accessibility counts by category for region {row['NAME_MAHAL']}:")
    for cat, count in accessibility_counts.items():
        logging.info(f" - {cat.capitalize()}: {count} places within threshold")

    logging.info(f"Weighted accessibility score for region {row['NAME_MAHAL']}: {weighted_score}")

    scores.append(weighted_score)
    logging.info(f"score process done for region number {idx} out of {len(regions)}")

regions["score"] = scores
regions.to_file("results/regions_result.shp")
logging.info("15-Minute accessibility analysis complete.")

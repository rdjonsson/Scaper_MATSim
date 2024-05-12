# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 09:13:05 2024

This file is used to create shapefile from MATSim *.xml network files, to 
facilitate visualization in qgis. 


@author: naqavi
"""



import geopandas as gpd
from shapely.geometry import Point, LineString
import xml.etree.ElementTree as ET
import os


project_dir = r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\src\main\resources\project'
os.makedirs(project_dir, exist_ok=True)

# Parse the XML file
tree = ET.parse(r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\src\main\resources\network_raw_noshorts.xml')
root = tree.getroot()

nodes_coordinates = {}

# Parse nodes
for node in root.iter("node"):
    node_id = node.get("id")
    node_x = float(node.get("x"))
    node_y = float(node.get("y"))
    nodes_coordinates[node_id] = (node_x, node_y)

# Create a list to store the link data
links_data = []

# Parse links
for link in root.iter("link"):
    link_id = link.get("id")
    from_node = link.get("from")
    to_node = link.get("to")
    
    # Check if the from and to nodes are in the dictionary
    if from_node in nodes_coordinates and to_node in nodes_coordinates:
        # Create LineString geometry using node coordinates
        link_geometry = LineString([nodes_coordinates[from_node], nodes_coordinates[to_node]])
        links_data.append({"id": link_id, "geometry": link_geometry})

# Create a GeoDataFrame for links
links_gdf = gpd.GeoDataFrame(links_data, geometry="geometry")
# Save GeoDataFrames as shapefiles
links_gdf.to_file(r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\src\main\resources\links.shp')

# Parse nodes
nodes_data = []
for node_id, (x, y) in nodes_coordinates.items():
    nodes_data.append({"id": node_id, "geometry": Point(x, y)})

# Create a GeoDataFrame for nodes
nodes_gdf = gpd.GeoDataFrame(nodes_data, geometry="geometry")
nodes_gdf.to_file(r'C:\Users\naqavi\OneDrive - KTH\!MATSim\Sthlm-try1\src\main\resources\nodes.shp')

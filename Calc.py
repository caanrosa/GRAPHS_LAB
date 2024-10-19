from Graph import Graph
import csv
import os
from math import sin, cos, sqrt, atan2, radians

# Nos piden que el valor de la distancia sea el  peso  de  la  arista que conecte dos aeropuertos
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    
    R = 6373.0  # Radio de la Tierra en km
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine (Una fórmula ahí que vi en Stack Overflow :v)
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance
    

g = Graph()
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "dataset/flights_final.csv")
try:
    with open(file_path, mode='r') as file:
        lector_csv = csv.DictReader(file)
        for fila in lector_csv:
            start = fila['Source Airport Code']  
            final = fila['Destination Airport Code']  
            g.add_edge(start, fila)  # Agregar el nodo del aeropuerto de origen
            g.add_edge(final)  # Agregar el nodo del aeropuerto de destino
            
except FileNotFoundError:
    print(f"El archivo {file_path} no existe.")
try:
    with open(file_path, mode='r') as file:
        lector_csv = csv.DictReader(file)
        for fila in lector_csv:
            lat1 = fila['Source Airport Latitude']
            lon1 = fila['Source Airport Longitude']
            lat2 = fila['Destination Airport Latitude']
            lon2 = fila['Destination Airport Longitude']
            weight = calculate_distance(lat1,lon1,lat2,lon2)
            g.add_edge(start, final, weight)  

except FileNotFoundError:
    print(f"El archivo {file_path} no existe.")



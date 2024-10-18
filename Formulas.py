from Grafo import *
import math
import csv
import os

def distancia_Mapa(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencia de coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia en kilómetros
    distancia = R * c
    return distancia
    

# ejemplo de como funciona
# lat1, lon1 = 40.416775, -3.703790  # Madrid
#lat2, lon2 = 48.856614, 2.3522219  # París

#distancia = distancia_Mapa(lat1, lon1, lat2, lon2)
#print(f"La distancia entre Madrid y París es de {distancia:.2f} km")

grafo = Grafo()
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "dataset/flights_final.csv")
try:
    with open(file_path, mode='r') as file:
        lector_csv = csv.DictReader(file)
        for fila in lector_csv:
            origen = fila['Source Airport Code']  
            destino = fila['Destination Airport Code']  
            grafo.agregar_nodo(origen)  # Agregar el nodo del aeropuerto de origen
            grafo.agregar_nodo(destino)  # Agregar el nodo del aeropuerto de destino
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
            peso = distancia_Mapa(lat1,lon1,lat2,lon2)
            grafo.agregar_arista(nod1, nod2, peso)  

except FileNotFoundError:
    print(f"El archivo {file_path} no existe.")

# Mostrar el grafo
grafo.mostrar_grafo()


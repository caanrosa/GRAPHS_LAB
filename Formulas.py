from Grafo import *
from Mian import *
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



dirname = os.path.dirname(__file__)
file_path = dirname + "/dataset/short_dataset.csv" # uno con menos para poder VISUALIZARLO
tree = AVL("Ciudad del aeropuerto orige")
num = 10

with open(file_path, mode='r') as file:
    lector_csv = csv.DictReader(file)
    for indice, fila in enumerate(lector_csv, start=1):
        if indice == num:  # Procesar solo la fila que el usuario le pida
            #titulo = fila['Title']
            #datos = dict(fila)  # Convertir la fila en un diccionario
            tree.insert(fila)
            break  # Salir del bucle después de insertar la fila 10

with open(file_path, mode='r') as file:
    lector_csv = csv.DictReader(file)
    for fila in lector_csv:
        #titulo = fila['Title']
        #datos = dict(fila)  # Convertir la fila en un diccionario
        tree.insert(fila)

tree.graph("datasetCompleto").view()
tree.Validacion_dataset(1000000,1000000)


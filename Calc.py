from Graph import Graph
from util import calculate_distance
import csv
import os

# Nos piden que el valor de la distancia sea el  peso  de  la  arista que conecte dos aeropuertos

g = Graph(10000000)
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "dataset/flights_final.csv")
# Crear un diccionario para mapear los códigos de aeropuertos a enteros
airport_mapping = {}
current_id = 0

# Luego agregamos las aristas
try:
    with open(file_path, mode='r') as file:
        lector_csv = csv.DictReader(file)
        
        for fila in lector_csv:
            start = fila['Source Airport Code']
            final = fila['Destination Airport Code']

            # Procesar las coordenadas para calcular la distancia
            lat1 = float(fila['Source Airport Latitude'])
            lon1 = float(fila['Source Airport Longitude'])
            lat2 = float(fila['Destination Airport Latitude'])
            lon2 = float(fila['Destination Airport Longitude'])
            weight = calculate_distance(lat1, lon1, lat2, lon2)

            # Agregar la arista con el peso calculado
            g.add_edge(start, final, weight)

except FileNotFoundError:
    print(f"El archivo {file_path} no existe.")



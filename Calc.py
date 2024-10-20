from Graph import *
import csv
import os

# Nos piden que el valor de la distancia sea el  peso  de  la  arista que conecte dos aeropuertos
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "dataset/flights_final.csv")
# Crear un diccionario para mapear los códigos de aeropuertos a enteros
airport_mapping = {}
current_id = 0

# Crear el diccionario de aeropuertos
try:
    with open(file_path, mode='r', encoding="utf8") as file:
        lector_csv = csv.DictReader(file)
        
        for fila in lector_csv:
            source = Aeropuerto(fila)
            dest = Aeropuerto(fila, True)
            
            if source.code not in airport_mapping:
                airport_mapping.update({source.code: current_id})
                current_id = current_id + 1
            
            if dest.code not in airport_mapping:
                airport_mapping.update({dest.code: current_id})
                current_id = current_id + 1          

except FileNotFoundError:
    print(f"El archivo {file_path} no existe.")
    
# Luego agregamos las aristas
try:
    with open(file_path, mode='r', encoding="utf8") as file:
        lector_csv = csv.DictReader(file)
      
        g = Graph(airport_mapping)
        
        for fila in lector_csv:
            source = Aeropuerto(fila)
            dest = Aeropuerto(fila, True)
            source.index = airport_mapping[source.code]
            dest.index = airport_mapping[dest.code]
            
            # Agregar los aeropuertos si es necesario
            s = g.add_node(source)
            d = g.add_node(dest)

            # Agregar la arista
            e = g.add_edge(source, dest)            

except FileNotFoundError:
    print(f"El archivo {file_path} no existe.")
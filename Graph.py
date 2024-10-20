from typing import List
from Utils import *

class Aeropuerto:
    def __init__(self, data, dest: bool = False):
        self.index = None
        if not dest:
            self.code = data["Source Airport Code"]
            self.name = data["Source Airport Name"]
            self.city = data["Source Airport City"]
            self.country = data["Source Airport Country"]
            self.lat = float(data["Source Airport Latitude"])
            self.lon = float(data["Source Airport Longitude"])
        else:
            self.code = data["Destination Airport Code"]
            self.name = data["Destination Airport Name"]
            self.city = data["Destination Airport City"]
            self.country = data["Destination Airport Country"]
            self.lat = float(data["Destination Airport Latitude"])
            self.lon = float(data["Destination Airport Longitude"])
            
    def __str__(self):
        return f"[code: {self.code}, name: {self.name}, city: {self.city}, country: {self.country}, lat: {self.lat}, lon: {self.lon}]"

class Vuelo:
    def __init__(self, source: Aeropuerto, dest: Aeropuerto):
        self.source = source
        self.dest = dest
        self.distance = calculate_distance(self.source.lat, self.source.lon, self.dest.lat, self.dest.lon)
        
class Graph:
        
    def __init__(self, n: int):
        self.n = n
        self.L: List[List[int]] = [[] for _ in range(n)]
        self.Aero: List[Aeropuerto] = [None for _ in range(n)]
        
    def add_node(self, data: Aeropuerto):
        if(data.index < self.n and self.Aero[data.index] is None):            

            self.Aero[data.index] = data
            return True
        else:
            return False

    def add_edge(self, source: Aeropuerto, dest: Aeropuerto) -> bool:
        if 0 <= source.index < self.n and 0 <= dest.index < self.n:
            # Se agrega la arista en ambas direcciones
            self.L[source.index].append(dest.index)
            self.L[dest.index].append(source.index)
            return True
        return False
    
    def DFS(self, u: int) -> None:
        visit = [False] * self.n
        self.__DFS_visit(u, visit)

    def __DFS_visit(self, u: int, visit: List[bool]) -> List[bool]:
        visit[u] = True
        print(self.Aero[u], end = ' ')
        for v in self.L[u]:
            if not visit[v]:
                visit = self.__DFS_visit(v, visit)
        return visit
    
    def is_connected(self) -> bool:
        
        visit = [False] * self.n # Crea una lista e inicia todos los nodos como no visitados
    
        visit = self.__DFS_visit(0, visit)  

        if all(visit):
            print("El grafo es conexo.")
            return True
        else:
            print("El grafo no es conexo.")
            return False
        
    def get_components(self):
        # Encuentra todas las componentes conexas en caso de que no sea conexo
        visit = [False] * self.n
        components = []
        
        for i in range(self.n):
            if not visit[i]:
                component = []
                visit = self.__DFS_visit_component(i, visit, component)
                components.append(component)

        return components
    
    def __DFS_visit_component(self, u: int, visit: List[bool], component: List[int]) -> List[bool]:
        visit[u] = True
        component.append(u)
        for v in self.L[u]:
            if not visit[v]:
                visit = self.__DFS_visit_component(v, visit, component)
        return visit
    
    def verify_connectivity(self) -> None:
        if self.is_connected():
            print("El grafo es conexo.")
        else:
            components = self.get_components()
            print("El grafo tiene", len(components), " componentes.")
            for i in range(len(components)):
                print(f"Componente {i + 1}: {components[i]} con {len(components[i])} vértices.")
                
    def prim(self):
        
        q = []  
        Tv = [0]  # nodo 0
        Te = []  # aristas en el árbol mínimo

        for vi in self.L[0]:
            weight = calculate_distance(self.Aero[0].lat, self.Aero[0].lon, self.Aero[vi].lat, self.Aero[vi].lon)
            q.append((weight, (0, vi)))

        q.sort(key=lambda x: x[0])  # Ordenar por el peso de las aristas

        while len(Tv) < self.n and q:
            weight, (vo, vi) = q.pop(0)  # Extraer la arista de menor peso
            if vi not in Tv:
                Tv.append(vi)
                Te.append((weight, (vo, vi)))

                
                for vk in self.L[vi]:
                    if vk not in Tv:
                        new_weight = calculate_distance(self.Aero[vi].lat, self.Aero[vi].lon, self.Aero[vk].lat, self.Aero[vk].lon)
                        q.append((new_weight, (vi, vk)))

                q.sort(key=lambda x: x[0])  # Reordenar la cola de prioridad

        return Te           
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
    
    # def Prim(self):
    #     in_mst = [False] * self.n          # Para saber si el nodo ya está en el MST
    #     key_values = [float('inf')] * self.n # Para almacenar los pesos mínimos encontrados
    #     parents = [-1] * self.n            # Almacena los padres de cada nodo en el MST

    #     key_values[0] = 0 # Empezamos desde el nodo 0
    #     total_weight = 0

    #     print("Arista \tPeso")
    #     for _ in range(self.n):
    #         # Encuentra el nodo u con el valor mínimo que no está en el MST
    #         u = min((v for v in range(self.n) if not in_mst[v]), key=lambda v: key_values[v])

    #         in_mst[u] = True
    #         # Si el nodo tiene un padre, imprime la arista y el peso correspondiente
    #         if parents[u] != -1:
    #             weight = self.weights[u][parents[u]]
    #             print(f"{parents[u]}-{u} \t{weight}")
    #             total_weight += weight

    #         # Explora los vecinos del nodo u
    #         for v in self.L[u]:
    #             if not in_mst[v] and self.weights[u][v] < key_values[v]:
    #                 key_values[v] = self.weights[u][v]
    #                 parents[v] = u

    #     print(f"Peso total del árbol de expansión mínima: {total_weight}")
        
    #     return 


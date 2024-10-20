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
            # print(data.index)
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

    # def prim(self, nodo_inicial):
    #     # Implementación del algoritmo de Prim para hallar el MST desde un nodo inicial
    #     visitado = {nodo: False for nodo in self.nodos}
    #     min_heap = [(0, nodo_inicial)]  # (peso, nodo)
    #     peso_total = 0

    #     while min_heap:
    #         peso, nodo = heapq.heappop(min_heap)
    #         if not visitado[nodo]:
    #             visitado[nodo] = True
    #             peso_total += peso
    #             for vecino, peso_arista in self.aristas[nodo]:
    #                 if not visitado[vecino]:
    #                     heapq.heappush(min_heap, (peso_arista, vecino))
    #     return peso_total

    # def dfs(self, nodo, visitado):
    #     # Exploración DFS para obtener todos los nodos en una componente conexa
    #     stack = [nodo]
    #     componente = []
    #     while stack:
    #         actual = stack.pop()
    #         if not visitado[actual]:
    #             visitado[actual] = True
    #             componente.append(actual)
    #             for vecino, _ in self.aristas[actual]:
    #                 if not visitado[vecino]:
    #                     stack.append(vecino)
    #     return componente

    # def calcular_MST_por_componente(self):
    #     visitado = {nodo: False for nodo in self.nodos}
    #     pesos_mst = []

    #     # Explorar cada componente del grafo
    #     for nodo in self.nodos:
    #         if not visitado[nodo]:
    #             # Explorar la componente conexa del nodo usando DFS
    #             componente = self.dfs(nodo, visitado)
    #             # Aplicar Prim desde cualquier nodo de la componente
    #             peso_mst = self.prim(componente[0])
    #             pesos_mst.append(peso_mst)
        
    #     return pesos_mst


 # def prim(self, nodo_inicial):
    #     # Implementación del algoritmo de Prim para hallar el MST desde un nodo inicial
    #     visitado = {nodo: False for nodo in self.nodos}
    #     min_heap = [(0, nodo_inicial)]  # (peso, nodo)
    #     peso_total = 0

    #     while min_heap:
    #         peso, nodo = heapq.heappop(min_heap)
    #         if not visitado[nodo]:
    #             visitado[nodo] = True
    #             peso_total += peso
    #             for vecino, peso_arista in self.aristas[nodo]:
    #                 if not visitado[vecino]:
    #                     heapq.heappush(min_heap, (peso_arista, vecino))
    #     return peso_total



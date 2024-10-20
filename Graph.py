from typing import List
from Utils import *
import networkx as nx
import matplotlib.pyplot as plt
from math import isinf

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
        return "{" + f"code: {self.code}, name: {self.name}, city: {self.city}, country: {self.country}, lat: {self.lat}, lon: {self.lon}" + "}"

class Graph:

    def __init__(self, dictionary: dict):
        self.airports_dict = dictionary
        self.view = nx.Graph()
        self.n = len(dictionary)
        self.L: List[List[int]] = [[] for _ in range(self.n)]
        self.Aero: List[Aeropuerto] = [None for _ in range(self.n)]        
        
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
            
            self.view.add_edge(source.index, dest.index)
            return True
        return False
    
    def __index_min_notvisited(self, arr: List[float], visit: List[bool]) -> int:    
        min = float("inf")
        entered = False
        
        for i, elem in enumerate(arr):                
            if(not visit[i]):
                if(elem < min):
                    entered = True
                    min = elem
                    
        #print("==========")
                    
        return arr.index(min)
    
    def get_info(self, code: str) -> Aeropuerto:
        return self.Aero[self.airports_dict[code]]
    
    # Conseguir los caminos minimos en una componente
    def dijkstra(self, v0: int = 0):
        
        D = [float("inf")] * self.n
        pad = [None] * self.n
        visit = [False] * self.n
        D[v0] = 0
        
        # Sacar del algoritmo los nodos que no están en la componente
        components = self.get_components()
        nodes = None
        for component in components:
            if(v0 in component): nodes = component
            else: 
                for i in component:
                    visit[i] = True
        
        #print(nodes)
        
        while(not all(visit)):
            # Seleccionar el menor que no haya sido visitado
            v = self.__index_min_notvisited(D, visit)
            visit[v] = True
            
            # Si el nodo no se encuentra en la componente de v0, evitar
            if(v not in nodes): 
                for ady in self.L[v]:
                    visit[ady] = True                    
            else:
                for i in self.L[v]:
                    weight = calculate_distance(self.Aero[v].lat, self.Aero[v].lon, self.Aero[i].lat, self.Aero[i].lon)                
                        
                    if(D[v] + weight < D[i] and not visit[i]):
                        D[i] = D[v] + weight
                        pad[i] = v
        
        for index, element in enumerate(D):
            if isinf(element):
                D[index] = "!TOREMOVE"
                pad[index] = "!TOREMOVE"
        
        # Se eliminan aquellos nodos que tienen distancia infinita (no hacen parte de la componente)
        D = list(filter(lambda x: x != "!TOREMOVE", D))
        pad = list(filter(lambda x: x != "!TOREMOVE", pad))
            
        return D, pad
    
    def largest_paths(self, v0: int = 0, size: int = 10) -> List[tuple[Aeropuerto, float]]:
        distances, parents = self.dijkstra(v0)
        
        sortedlist = distances.copy()
        sortedlist.sort(reverse=True)
        
        returnable = []
        
        for index in range(0, size):
            aeroIndex = distances.index(sortedlist[index])
            returnable.append((self.Aero[aeroIndex], sortedlist[index]))
            
        return returnable
    
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
        
    def get_components(self) -> List[List[int]]:
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
                
    def show(self):
        node_labels = {}
        node_positions = {}
        for a in self.Aero:
            if(a):
                node_labels.update({a.index: a.code})
                node_positions.update({a.index: (a.lon, a.lat)})
        
        print(f"Graficando {self.view.number_of_nodes()} nodos")
        
        nx.draw_networkx(self.view, with_labels = True,
                pos = node_positions,
                labels = node_labels,
                font_size = 7,
                node_size = [len(v)**2 * 35 for key, v in node_labels.items()],
                )
        
        print("Mostrando")
        plt.show()
       
    # Mostrar el camino más corto entre dos vertices 
    def show(self, v0: int, vf: int):
        G = nx.Graph()
        dist, pad = self.dijkstra(v0)
        
        node_list: List[Aeropuerto] = []
        
        i = vf
        while(i != v0):
            #print(i)
            u1 = self.Aero[pad[i]]
            u2 = self.Aero[i]
            G.add_edge(u1.index, u2.index, weight = calculate_distance(u1.lat, u1.lon, u2.lat, u2.lon))
            node_list.append(self.Aero[i])
            i = pad[i]
        
        node_list.append(self.Aero[v0])
        
        node_labels = {}
        node_positions = {}
        for a in node_list:
            print(a)
            node_labels.update({a.index: a.code})
            node_positions.update({a.index: (a.lon, a.lat)})
                
                
        print(f"Graficando {len(node_list)} nodos")
        
        # ARISTAS
        nx.draw_networkx_edges(
            G, pos = node_positions, width=5, alpha=0.5, edge_color="black"
        )
        
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos = node_positions, edge_labels = edge_labels, font_size = 8)
        
        # NODOS
        nx.draw_networkx_nodes(G, 
            pos = node_positions, 
            node_size = [len(v)**2 * 35 for key, v in node_labels.items()],            )
        
        # node labels
        nx.draw_networkx_labels(G,
            pos = node_positions,
            labels= node_labels,
            font_size = 7,
            font_family="sans-serif")

        print("Mostrando")
        
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

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



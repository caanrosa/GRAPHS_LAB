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
    
    def get_info(self, code: str) -> Aeropuerto | None:
        try: 
            return self.Aero[self.airports_dict[code]]
        except KeyError:
            printSubtitle("No se encontró ese aeropuerto")
            return None
    
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
        
        if(size > len(sortedlist)): size = len(sortedlist) - 1
        
        for index in range(0, size):
            aeroIndex = distances.index(sortedlist[index])
            returnable.append((self.Aero[aeroIndex], sortedlist[index]))
            
        return returnable
    
    def DFS(self, u: int) -> None:
        visit = [False] * self.n
        self.__DFS_visit(u, visit)

    def __DFS_visit(self, u: int, visit: List[bool]) -> List[bool]:
        visit[u] = True
        #print(self.Aero[u], end = ' ')
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
        if not self.is_connected():
            components = self.get_components()
            print("El grafo tiene", len(components), " componentes.")
            for i in range(len(components)):
                print(f"Componente {i + 1}: ", end="")
                for index in components[i]:
                    print(f"{self.Aero[index].code} {self.Aero[index].name}")
                
                print(f"con {len(components[i])} vértices.")
                print()             
    
    def show_all(self):
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
        # Sacar del algoritmo los nodos que no están en la componente
        same = False
        components = self.get_components()
        for component in components:
            if(v0 in component): 
                if (vf in component):
                    same = True
                    break
        
        if(not same): return False
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
            printSubtitle(f"[{a.code}] {a.name}\nUbicación: {a.city}, {a.country} ({a.lat} {a.lon}).")
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
                
    def prim(self, component):
        if len(component) <= 1:
            return 0  # Si la componente tiene 1 solo nodo, el MST es 0.
        
        q = []
        total_weight = 0  
        Tv = [component[0]]  # nodo 0
        Te = []  # aristas en el árbol mínimo

        for vi in self.L[component[0]]:
            if vi in component:
                peso = calculate_distance(self.Aero[component[0]].lat, self.Aero[component[0]].lon, self.Aero[vi].lat, self.Aero[vi].lon)
                q.append((peso, (component[0], vi)))

        q.sort(key=lambda x: x[0])  # Ordenar por el peso de las aristas

        while len(Tv) < len(component) and q:
            weight, (vo, vi) = q.pop(0)  # Extraer la arista de menor peso
            if vi not in Tv:
                print(f"Agregando arista: ({self.Aero[vo].code}, {self.Aero[vi].code}) con peso: {weight}")
                Tv.append(vi)
                Te.append((weight, (vo, vi)))
                total_weight += weight

                for vk in self.L[vi]:
                    if vk not in Tv and vk in component:
                        peso_nuevo = calculate_distance(self.Aero[vi].lat, self.Aero[vi].lon, self.Aero[vk].lat, self.Aero[vk].lon)
                        q.append((peso_nuevo, (vi, vk)))
        
                q.sort(key=lambda x: x[0])  # Reordenar la "cola de prioridad"

        return total_weight      
    
    def calculate_components_MST_weight(self):
        
        components = self.get_components()
        total_weight_all_components = 0
        # Una componente
        if len(components) == 1:
            total_weight = self.prim(components[0])
            print(f"Peso del árbol de expansión mínima: {total_weight}")
            return total_weight
        
        else:
            # Más de una componente
            all_weights = []
            i = 1  
            
            for component in components:
                print(f"\nCalculando MST para la componente {i}:")
                weight = self.prim(component)
                all_weights.append(weight)
                total_weight_all_components += weight  
                print(f"Peso del árbol de expansión mínima de la componente {i}: {weight}")  
                i += 1
                
            print(f"\nPeso total del árbol de expansión mínima de todas las componentes: {total_weight_all_components}")
            return all_weights                    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
    
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


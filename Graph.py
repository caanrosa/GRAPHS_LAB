import csv
import os
from typing import List
from Calc import *

class Graph:

    def __init__(self, n: int):
        self.n = n
        self.L: List[List[int]] = [[] for _ in range(n)] 

    def add_edge(self, u: int, v: int) -> bool:
        if 0 <= u < self.n and 0 <= v < self.n:
            # Se agrega la arista en ambas direcciones
            self.L[u].append((v, weight))
            self.L[v].append((u, weight))
            return True
        return False
    
    def DFS(self, u: int) -> None:
        visit = [False] * self.n
        self.__DFS_visit(u, visit)

    def __DFS_visit(self, u: int, visit: List[bool]) -> List[bool]:
        visit[u] = True
        print(u, end = ' ')
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



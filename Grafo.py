from Cordenadas import *
from Mian import *

class Grafo:
    def __init__(self):
        # Diccionario para almacenar los nodos con sus atributos
        # Cada nodo apunta a otro diccionario con los atributos del nodo
        self.nodos = {}
        
        # Diccionario para almacenar las aristas
        # Cada nodo apunta a una lista de pares (nodo vecino, peso)
        self.aristas = {}

    def agregar_nodo(self, nodo, **atributos):
        # Añadir el nodo con sus atributos
        if nodo not in self.nodos:
            self.nodos[nodo] = atributos
            self.aristas[nodo] = []

    def agregar_arista(self, nodo1, nodo2, peso):
        # Asegurarse de que los nodos existan en el grafo
        if nodo1 not in self.nodos:
            self.agregar_nodo(nodo1)
        if nodo2 not in self.nodos:
            self.agregar_nodo(nodo2)

        # Añadir arista de nodo1 a nodo2 con peso
        self.aristas[nodo1].append((nodo2, peso))
        
        # Como es un grafo no dirigido, añadir la arista de nodo2 a nodo1 también
        self.aristas[nodo2].append((nodo1, peso))

    def mostrar_grafo(self):
        # Mostrar los nodos con sus atributos
        print("Nodos y sus atributos:")
        for nodo, atributos in self.nodos.items():
            print(f"Nodo {nodo}: {atributos}")
        
        # Mostrar la representación del grafo
        print("\nAristas:")
        for nodo in self.aristas:
            print(f"Nodo {nodo}: {self.aristas[nodo]}")
    
    def prim(self, nodo_inicial):
        # Implementación del algoritmo de Prim para hallar el MST
        visitado = [False] * self.V
        min_heap = [(0, nodo_inicial)]  # (peso, nodo)
        peso_total = 0
        while min_heap:
            peso, nodo = heapq.heappop(min_heap)
            if not visitado[nodo]:
                visitado[nodo] = True
                peso_total += peso
                for vecino, peso_arista in self.grafo[nodo]:
                    if not visitado[vecino]:
                        heapq.heappush(min_heap, (peso_arista, vecino))
        return peso_total

    def calcular_MST_por_componente(self):
        visitado = [False] * self.V
        pesos_mst = []
        for nodo in range(self.V):
            if not visitado[nodo]:
                # Explorar la componente conexa del nodo
                componente = self.dfs(nodo, visitado)
                # Aplicar Prim desde cualquier nodo de la componente
                peso_mst = self.prim(componente[0])
                pesos_mst.append(peso_mst)
        return pesos_mst

# Ejemplo de uso
mi_grafo = Grafo()

# Agregar nodos con atributos
mi_grafo.agregar_nodo(1, color="rojo", tamaño=10)
mi_grafo.agregar_nodo(2, color="azul", tamaño=15)
mi_grafo.agregar_nodo(3, color="verde", tamaño=12)

# Agregar aristas ponderadas
mi_grafo.agregar_arista(1, 2, 4)
mi_grafo.agregar_arista(1, 3, 2)
mi_grafo.agregar_arista(2, 3, 5)

# Mostrar el grafo
mi_grafo.mostrar_grafo()
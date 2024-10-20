
from Graph import *
from Calc import *

f = Graph(100)
running = True

while(running): 
    print("MENU PRINCIPAL")
    printOption(1, "Grafo generado es conexo o no")
    printOption(2, "Determinar peso del árbol a partir del nodo")
    printOption(3, "Mostrar informacion")
    printOption(0, "SALIR")
    
    option = f.getInputInt()
    printBottom()
    
    match option:
        case 0:
            running = False
            
        case 1:
            r = f.is_connected()
            if r:
                pArint("El grafo es conexo.")
            else:
                print("El grafo no es conexo.")    

        case 2:
            correct = f.calculate_components_MST_weight()        
        case 3:
            printTitle("Mostrar informacion")
            printop(1,"informacion del aeropuerto")
            printop(2,"informacion del aeropuerto de los 10 caminos minimos mas largos")
            printop(3,"mostrar camino minimo entre el primero y segundo vertice")
            op = getInputInt()
            printBottom()
            match op:
                case 1:
                    print("hola")
                case 2:
                    print("hola")
                case 3:
                    print("hola")

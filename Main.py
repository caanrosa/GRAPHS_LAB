
from Graph import *
from Calc import *

f = generate()
running = True

while(running): 
    printTitle("MENU PRINCIPAL")
    printOption(1, "Grafo generado es conexo o no")
    printOption(2, "Determinar peso del árbol a partir del nodo")
    printOption(3, "Mostrar informacion")
    printOption(0, "SALIR")
    
    option = getInputInt()
    printBottom()
    
    match option:
        case 0:
            running = False
            
        case 1:
            r = f.is_connected()

        case 2:
            correct = f.calculate_components_MST_weight()        
        case 3:
            printTitle("Mostrar informacion")
            printOption(1,"informacion del aeropuerto")
            printOption(2,"informacion del aeropuerto de los 10 caminos minimos mas largos")
            printOption(3,"mostrar camino minimo entre el primero y segundo vertice")
            op = getInputInt()
            printBottom()
            match op:
                case 1:
                    printSubtitle("Escriba un codigo")
                    code = getInput()
                    f.get_info(code)
                case 2:
                    printSubtitle("Escriba un codigo")
                    code = getInput()
                    r = f.get_info(code.upper())
                    v = f.largest_paths(r.index)
                   
                    for elemento in v:
                        a = elemento[0]
                        b = elemento[1]
                        printSubtitle(f"Aeropuerto {a.city} {a.code} {a.index} {a.lat} {a.lon} {a.name} Peso {b}")

                case 3:
                    printSubtitle("Escriba el codigo del aeropuesto de salida")
                    code1 = getInput()
                    r1 = f.get_info(code1.upper())
                    printSubtitle("Escriba el codigo del aeropuesto de entrada")
                    code2 = getInput()
                    r2 = f.get_info(code2.upper())
                    f.show(r1.index,r2.index)

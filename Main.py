
from Graph import *
from Calc import *

f = generate()
running = True

while(running): 
    printTitle("MENU PRINCIPAL")
    printOption(1, "Grafo generado es conexo o no")
    printOption(2, "Determinar peso del árbol de expansión mínima")
    printOption(3, "Mostrar información")
    printOption(4, "Mostrar grafo generado")
    printOption(0, "SALIR")
    
    option = getInputInt()
    printBottom()
    
    match option:
        case 0:
            running = False
            
        case 1:
            f.verify_connectivity()

        case 2:
            correct = f.calculate_components_MST_weight()        
        case 3:
            printTitle("Mostrar información")
            printOption(1, "Informacion del aeropuerto")
            printOption(2, "Informacion del aeropuerto: 10 caminos mínimos más largos")
            printOption(3, "Mostrar camino minimo entre dos vértices")
            op = getInputInt()
            printBottom()
            match op:
                case 1:
                    printSubtitle("Escriba un codigo")
                    code = getInput()
                    info = f.get_info(code.upper())
                    
                    if(info): printSubtitle(f"[{info.code}] {info.name}\nUbicación: {info.city}, {info.country} ({info.lat} {info.lon}).")
                case 2:
                    printSubtitle("Escriba un codigo")
                    code = getInput()
                    r = f.get_info(code.upper())
                    if(r):
                        v = f.largest_paths(r.index)
                    
                        for elemento in v:
                            a = elemento[0]
                            b = elemento[1]
                            
                            printSubtitle(f"[{a.code}] {a.name}\nUbicación: {a.city}, {a.country} ({a.lat} {a.lon}).\nDistancia: {b} km")

                case 3:
                    printSubtitle("Escriba el codigo del aeropuesto de salida")
                    code1 = getInput()
                    r1 = f.get_info(code1.upper())
                    if(r1):
                        printSubtitle("Escriba el codigo del aeropuesto de entrada")
                        code2 = getInput()
                        r2 = f.get_info(code2.upper())
                        
                        if(r2): f.show(r1.index,r2.index)
        case 4:
            f.show_all()
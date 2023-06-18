# Kleinübing Germán, Salemme Christian, Díaz Lola, García Pilar
import random
from colorama import init, Fore, Style

def carga_puntuacion(puntos_jugador, puntos_cpu, mazo_valores_usuario, mazo_valores_maquina):
    dic_tipos={"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "+2":20, "X":20, "!!":50, "+4":50}
    sumador=0
    key=""
    if len(mazo_valores_usuario)==0:
        for j in range(len(mazo_valores_maquina)):
            key=str(mazo_valores_maquina[j])
            sumador+=dic_tipos[key]
        puntos_cpu+=sumador
        return puntos_cpu, puntos_jugador
    else:
        for i in range(len(mazo_valores_usuario)):
            key=str(mazo_valores_usuario[i])
            sumador+=dic_tipos[key]
        puntos_jugador+=sumador
        return puntos_cpu, puntos_jugador
        
def rellenar_mazo(mazo, filas, columnas):
    for f in range(filas):
        for c in range (columnas):
            mazo[f][c]= 1 if c==0 or c>=12 else 2
            
def posycarta_random(todos_los_colores, todos_los_tipos): 
    pos_col=random.randint(0, 3)
    pos_tipo=random.randint(0,13)
    carta_col=todos_los_colores[pos_col]
    carta_tipo=todos_los_tipos[pos_tipo]
    return carta_col, carta_tipo, pos_col, pos_tipo

def repartir_cartas(jugador_color, jugador_tipo, mazo, todos_los_colores, todos_los_tipos): 
    i=0
    while i<=len(jugador_color)-1:
        color, tipo, pos_color, pos_tipo=posycarta_random(todos_los_colores, todos_los_tipos)
        if mazo[pos_color][pos_tipo]!=0:
            jugador_color[i]=color if 12 != pos_tipo != 13 else ""
            jugador_tipo[i]=tipo
            mazo[pos_color][pos_tipo]-=1
            i+=1

def inicio_medio(mazo, todos_los_colores, todos_los_tipos):
    medio = []
    color, tipo, pos_color, pos_tipo=posycarta_random(todos_los_colores, todos_los_tipos)
    while mazo[pos_color][pos_tipo] == 0 or pos_tipo > 9:
        color, tipo, pos_color, pos_tipo=posycarta_random(todos_los_colores, todos_los_tipos)
    medio.append(color)
    medio.append(tipo)
    mazo[pos_color][pos_tipo]-=1
    return medio

def ingresa_valida(msj, msj_error, cond1, cond2, cond3="nada", cond4="nada"):
    respuesta=(input(msj)).upper()    
    while respuesta != cond1 and respuesta != cond2 and respuesta != cond3 and respuesta != cond4:
        print(msj_error)
        respuesta=(input(msj)).upper()
    return respuesta

def validar_tirada(pos, jugador_color, jugador_tipo, medio, todos_los_colores, todos_los_tipos, mazo, cant_sumar, intento = 0):
    imprimir_blanco()
    if jugador_tipo[pos] == "!!" or jugador_tipo[pos] == "+4":
        col_nuevo=ingresa_valida("\nIngrese el nuevo color.\n(Rojo=R, Azul=AZ, Amarrillo=AM, Verde=V): ", "\nPor favor, responda con alguna de las letras válidas.", "R", "AZ", "AM", "V")
        carta_medio(pos, medio, jugador_color, jugador_tipo, col_nuevo)
        eliminar_cartas(pos, jugador_color, jugador_tipo)
        confirma_tiro = 1
        return confirma_tiro
    
    elif medio[0] == jugador_color[pos] or medio[1] == jugador_tipo[pos]:
        carta_medio(pos, medio, jugador_color, jugador_tipo)
        eliminar_cartas(pos, jugador_color, jugador_tipo)
        confirma_tiro = 1
        return confirma_tiro
    
    else:
        if intento == 0:
            print("¡No puede tirar esa carta intente nuevamente!")
            accion_usuario(medio, usuario_color, usuario_tipo, mazo, todos_los_colores, todos_los_tipos, cant_sumar, 0)
        else:
            print("¡No puede tirar esa carta intente nuevamente!")
            accion_usuario(medio, usuario_color, usuario_tipo, mazo, todos_los_colores, todos_los_tipos, cant_sumar, 1)
            
def tirar_cartas(medio, jugador_color, jugador_tipo, todos_los_colores, todos_los_tipos, mazo, cant_sumar):
    while True:
        try:
            imprimir_blanco()
            pos_tirar=int(input("¿Qué carta?, Escriba la posición de la carta: "))-1
            while pos_tirar < 0 or pos_tirar > len(jugador_tipo):
                print("Escriba un posición de carta válida.")
                pos_tirar=int(input("¿Qué carta?, Escriba la posición de la carta: "))-1
            confirma_tiro = validar_tirada(pos_tirar, jugador_color, jugador_tipo, medio, todos_los_colores, todos_los_tipos, mazo, cant_sumar)
            return confirma_tiro
        except ValueError:
            print("La posición debe ser un valor numerico")

        except IndexError:
            print("Posición erronea, intente nuevamente")

def es_mazo_vacio(mazo):
    contador=0
    for f in range(4):
        for c in range(14):
            if mazo[f][c]==0:
                contador+=1
    if contador==56:
        return True
    else:
        return False
                    
def agarrar_cartas(mazo, jugador_color, jugador_tipo, medio, todos_los_colores, todos_los_tipos, usuario=0, cant_sumar=1):
    valor=es_mazo_vacio(mazo)
    if valor:
        rellenar_mazo(mazo, 4, 14)
    
    i=0
    while i < cant_sumar:
        color, tipo, pos_color, pos_tipo=posycarta_random(todos_los_colores, todos_los_tipos)
        if mazo[pos_color][pos_tipo]!=0:
            if 12 != pos_tipo != 13:
                jugador_color.append(color)
                jugador_tipo.append(tipo)
                mazo[pos_color][pos_tipo]-=1
                i+=1
                if usuario == 0:
                    imprimir_blanco()
                    print("Nueva carta: ")
                    if tipo == "!!" or tipo == "+4":
                        print(tipo)
                    else:
                        print(color, tipo)
                        
                    if cant_sumar == 1:    
                        resp=ingresa_valida("¿Desea tirar la carta al pozo?(si/no): ", "\nPor favor, responda con sí o no.", "SI", "NO")
                        if resp == "SI":
                            pos=len(jugador_tipo)-1
                            confirma_tiro = validar_tirada(pos, jugador_color, jugador_tipo, medio, todos_los_colores, todos_los_tipos, mazo, cant_sumar, 1)
                            return confirma_tiro
                        else:
                            confirma_tiro = 0
                            return confirma_tiro
                            
            else:
                jugador_color.append("")
                jugador_tipo.append(tipo)
                mazo[pos_color][pos_tipo]-=1
                i+=1
                if usuario == 0:
                    imprimir_blanco()
                    print("Nueva carta: ")
                    if tipo == "!!" or tipo == "+4":
                        print(tipo)
                    else:
                        print(color, tipo)
                        
                    if cant_sumar == 1:    
                        resp=ingresa_valida("¿Desea tirar la carta al pozo?(si/no): ", "\nPor favor, responda con sí o no.", "SI", "NO")
                        if resp == "SI":
                            pos=len(jugador_tipo)-1
                            confirma_tiro = validar_tirada(pos, jugador_color, jugador_tipo, medio, todos_los_colores, todos_los_tipos, mazo, cant_sumar, 1)
                            return confirma_tiro
                        else:
                            confirma_tiro = 0
                            return confirma_tiro

def validar_uno(numeros, todos_los_colores, medio, usuario = 0):
    imprimir_blanco()
    uno = True
    if len(numeros) > 2:
        if usuario == 0:
            print("¡Es mentira, tiene mas de 2 cartas!")
        uno = False
    elif (medio[0] not in todos_los_colores and medio[1] not in numeros) and "" not in todos_los_colores:
        if usuario == 0:
            print("No tiene la posibilidad de tirar una carta.")
        uno = False
    if usuario != 0:
        if len(numeros) == 1:
            uno = False
    return uno

def carta_medio(pos, medio, jugador_color, jugador_tipo, col_nuevo= ""): 
    if col_nuevo != "":
        medio[0]=col_nuevo
    else:
        medio[0]=jugador_color[pos]
    medio[1]=jugador_tipo[pos]

def eliminar_cartas(pos, jugador_color, jugador_tipo): 
    jugador_color.pop(pos)
    jugador_tipo.pop(pos)
    
def elegir_color_cpu(color_cpu, todos_los_colores):
    if len(color_cpu) != 0:
        cantidad_color_max = -1
        for c in todos_los_colores:
            aux = color_cpu.count(c)
            if aux > cantidad_color_max:
                cantidad_color_max = aux
                color_max = c
        return color_max
    
def tirar_cartas_cpu(numeros_cpu, color_cpu, numeros_usuario, medio, mazo, todos_los_colores, todos_los_tipos, cant_sumar, intento=0):
    if len(numeros_usuario) < 3 and "+4" in numeros_cpu:
        posicion = numeros_cpu.index("+4")
        color_nuevo = elegir_color_cpu(color_cpu, todos_los_colores)
        carta_medio(posicion, medio, color_cpu, numeros_cpu, color_nuevo)
        eliminar_cartas(posicion, color_cpu, numeros_cpu)
        confirma_tiro = 1
        return confirma_tiro
    elif medio[0] in color_cpu:
        posicion = color_cpu.index(medio[0])
        carta_medio(posicion, medio, color_cpu, numeros_cpu)
        eliminar_cartas(posicion, color_cpu, numeros_cpu)
        confirma_tiro = 1
        return confirma_tiro
    elif medio[1] in numeros_cpu:
        posicion = numeros_cpu.index(medio[1])
        if color_cpu[posicion] == "":
            color_nuevo = elegir_color_cpu(color_cpu, todos_los_colores)
            carta_medio(posicion, medio, color_cpu, numeros_cpu, color_nuevo)
        else:
            carta_medio(posicion, medio, color_cpu, numeros_cpu)
        eliminar_cartas(posicion, color_cpu, numeros_cpu)
        confirma_tiro = 1
        return confirma_tiro
    elif "!!" in numeros_cpu:
        posicion = numeros_cpu.index("!!")
        color_nuevo = elegir_color_cpu(color_cpu, todos_los_colores)
        carta_medio(posicion, medio, color_cpu, numeros_cpu, color_nuevo)
        eliminar_cartas(posicion, color_cpu, numeros_cpu)
        confirma_tiro = 1
        return confirma_tiro
    elif "+4" in numeros_cpu:
        posicion = numeros_cpu.index("+4")
        color_nuevo = elegir_color_cpu(color_cpu, todos_los_colores)
        carta_medio(posicion, medio, color_cpu, numeros_cpu, color_nuevo)
        eliminar_cartas(posicion, color_cpu, numeros_cpu)
        confirma_tiro = 1
        return confirma_tiro
    else:
        if intento == 0:
            if es_mazo_vacio(mazo):
                rellenar_mazo(mazo, 4, 14)
            agarrar_cartas(mazo, color_cpu, numeros_cpu, medio, todos_los_colores, todos_los_tipos, 1, 1)
            confirma_tiro = tirar_cartas_cpu(numeros_cpu, color_cpu, numeros_usuario, medio, mazo, todos_los_colores, todos_los_tipos, cant_sumar, 1)
            return confirma_tiro
        
def leer_reglas():
    try:
        arch = open("reglas.txt", "rt")
        linea = arch.readline()
        while linea:
            print(linea)
            linea = arch.readline()
    except FileNotFoundError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    except OSError as mensaje:
        print("No se pudo leer el archivo", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass
        
def recuadro(colores, numerocarta, lista_colores):
    init()
    for i in range(len(numerocarta)):
        if lista_colores[i]==colores[0]:
            c=Fore.RED + Style.NORMAL
            imprimir_carta(c, numerocarta, i)
        elif lista_colores[i]==colores[1]:
            c=Fore.BLUE + Style.NORMAL
            imprimir_carta(c, numerocarta, i)
        elif lista_colores[i]==colores[2]:
            c=Fore.YELLOW + Style.NORMAL
            imprimir_carta(c, numerocarta, i)
        elif lista_colores[i]==colores[3]:
            c=Fore.GREEN + Style.NORMAL
            imprimir_carta(c, numerocarta, i)
        elif lista_colores[i] == "":
            print()
            print(Fore.RED + Style.NORMAL +" __")
            print(Fore.GREEN + Style.NORMAL +"|"+" "*2+"|")
            print(Fore.YELLOW + Style.NORMAL +"|"+numerocarta[i]+"|")
            print(Fore.BLUE + Style.NORMAL +"|"+"_"*2+"|",end="  ")

def imprimir_carta(cl, numerocarta, j):
    if numerocarta[j]=="+2" or numerocarta[j]=="!!" or numerocarta[j]=="+4":
        print()
        print(cl+" __")
        print(cl+"|"+" "*2+"|")
        print(cl+"|"+numerocarta[j]+"|")
        print(cl+"|"+"_"*2+"|",end="  ")
    else:
        print()
        print(cl+" __")
        print(cl+"|"+" "*2+"|")
        print(cl+"|"+numerocarta[j]+" "+"|")
        print(cl+"|"+"_"*2+"|",end="  ")

def printpozo(pozo):
    if pozo[0]=="R":
        c=Fore.RED + Style.NORMAL
        imprimir_carta(c, pozo, 1)
    elif pozo[0]=="AZ":
        c=Fore.BLUE + Style.NORMAL
        imprimir_carta(c, pozo, 1)
    elif pozo[0]=="AM":
        c=Fore.YELLOW + Style.NORMAL
        imprimir_carta(c, pozo, 1)
    elif pozo[0]=="V":
        c=Fore.GREEN + Style.NORMAL
        imprimir_carta(c, pozo, 1)
    elif pozo[0] == "":
        print()
        print(Fore.RED + Style.NORMAL +" __")
        print(Fore.GREEN + Style.NORMAL +"|"+" "*2+"|")
        print(Fore.YELLOW + Style.NORMAL +"|"+pozo[1]+"|")
        print(Fore.BLUE + Style.NORMAL +"|"+"_"*2+"|",end="  ")

def imprimir_blanco():
    init()
    print(Fore.WHITE+ Style.NORMAL +"")

def accion_usuario(medio, color_usuario, numero_usuario, mazo, todos_los_colores, todos_los_tipos, cant_sumar, intento = 0):
    imprimir_blanco() 
    accion=ingresa_valida("\n¿Qué desea hacer?\nTIRAR una carta = T\nAgarrar una carta del MAZO = M\nDecir UNO = UNO\n¿?: ", "\nPor favor, responda con alguna de las letras o palabras válidas.", "T", "M", "UNO")
    if accion == "T":
        confirma_tiro = tirar_cartas(medio, color_usuario, numero_usuario, todos_los_colores, todos_los_tipos, mazo, cant_sumar)
        olvido_uno(mazo, color_usuario, numero_usuario, todos_los_colores, todos_los_tipos, cant_sumar)
        confirma_robar=0
        return confirma_robar, confirma_tiro
    elif accion == "M":
        if intento == 0:
            confirma_tiro = agarrar_cartas(mazo, color_usuario, numero_usuario, medio, todos_los_colores, todos_los_tipos, cant_sumar)
            confirma_robar=0
            return confirma_robar, confirma_tiro
        else:
            print("¡Solo se puede agarrar una carta por vez!")
    elif accion == "UNO":
        if validar_uno(numero_usuario, color_usuario, medio):
            print("¡¡UNO!!")
            confirma_tiro = tirar_cartas(medio, color_usuario, numero_usuario, todos_los_colores, todos_los_tipos, mazo, cant_sumar)
            confirma_robar=0
            return confirma_robar, confirma_tiro
        else:
            accion_usuario(medio, color_usuario, numero_usuario, mazo, todos_los_colores, todos_los_tipos, cant_sumar, intento)
    else:
        print("Por favor, ingrese una opción válida")
        accion_usuario(medio, color_usuario, numero_usuario, mazo, todos_los_colores, todos_los_tipos, cant_sumar)
        
def olvido_uno(mazo, color_usuario, numero_usuario, todos_los_colores, todos_los_tipos, cant_sumar):
    imprimir_blanco() 
    if len(numero_usuario) == 1:
        print('-cpu: Te olvidaste de decir "UNO", agarras dos cartas.')
        agarrar_cartas(mazo, usuario_color, usuario_tipo, pozo, todos_los_colores, todos_los_tipos, 0, 2)

def inicializar_0(todos_los_colores, todos_los_tipos):
        
    mazo=[[0]*14 for i in range(4)]
    rellenar_mazo(mazo, 4, 14)

    pc_color=[0]*7
    pc_tipo=[0]*7
    usuario_color=[0]*7
    usuario_tipo=[0]*7
    
    a_sumar=0
    saltar_turno=False
    confirma_robar=0
    posicion=0
    confirma_tiro=0

    repartir_cartas(pc_color, pc_tipo, mazo, todos_los_colores, todos_los_tipos)
    repartir_cartas(usuario_color, usuario_tipo, mazo, todos_los_colores, todos_los_tipos)
        
    medio = inicio_medio(mazo, todos_los_colores, todos_los_tipos)
    print("\nPozo:")
    printpozo(medio)
        
    return mazo, pc_color, pc_tipo, usuario_color, usuario_tipo, medio, a_sumar, saltar_turno, confirma_robar, posicion

#programa principal

leer=ingresa_valida("¿Desea leer las reglas antes de empezar la partida? (si/no): ", "\nPor favor, responda con sí o no.", "SI", "NO")
if leer == "SI":
    leer_reglas()

modo=ingresa_valida("\nIndique la letra del modo que quiere jugar (R=rapido/P=puntos): ","\nPor favor, responda con alguna de las letras válidas." ,"R", "P")

colores=("R", "AZ", "AM", "V")
tipos=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "X", "!!", "+4")
puntos_del_usuario=0
puntos_de_la_maquina=0

matriz_mazo, pc_color, pc_tipo, usuario_color, usuario_tipo, pozo, sumarcartas, saltar_turno, confirma_robar, posicion= inicializar_0(colores, tipos)

while puntos_del_usuario < 500 and puntos_de_la_maquina < 500:
    imprimir_blanco()
    if (len(pc_tipo) == 0) or (len(usuario_tipo) == 0):
        if modo == "P":
            imprimir_blanco()
            puntos_de_la_maquina, puntos_del_usuario = carga_puntuacion(puntos_del_usuario, puntos_de_la_maquina, usuario_tipo, pc_tipo)
            print("PUNTOS DEL USUARIO")
            print(puntos_del_usuario)
            print("PUNTOS DE LA MAQUINA")
            print(puntos_de_la_maquina)
            if puntos_del_usuario > 500 and puntos_de_la_maquina > 500:
                break
            matriz_mazo, pc_color, pc_tipo, usuario_color, usuario_tipo, pozo, sumarcartas, saltar_turno, confirma_robar, posicion= inicializar_0(colores, tipos)
        else:
            break
        
    imprimir_blanco()
    print("\nTus cartas:")
    recuadro(colores, usuario_tipo, usuario_color)
    imprimir_blanco()
    if sumarcartas==0 or confirma_robar==0:
        sumarcartas=0
        if saltar_turno==False:
            
            confirma_robar, confirma_tiro = accion_usuario(pozo, usuario_color, usuario_tipo, matriz_mazo, colores, tipos, sumarcartas)
            
            if confirma_tiro==1:
                if pozo[1]=="+2":
                    sumarcartas+=2
                    confirma_robar=1
                    confirma_tiro=0
                if pozo[1]=="+4":
                    sumarcartas+=4
                    confirma_tiro=0
                    confirma_robar=1
                if pozo[1]=="X":
                    saltar_turno=True
                    confirma_tiro=0
            else:
                confirma_tiro=0
                
        else:
            imprimir_blanco()
            print("Se cancelo su turno por carta X.")
            saltar_turno=False
    else:
        confirma_accion=1
        while confirma_accion !=0 :
            
            decision=ingresa_valida('¿Desea tirar una carta "+2" o "+4"? (si/no): ', "\nPor favor, responda con sí o no.", "SI", "NO")
            if decision == "SI":
                pos_tirar=int(input("¿Qué carta?, Escriba la posición de la carta: "))-1
                while pos_tirar < 0 or pos_tirar > len(usuario_tipo):
                    print("Escriba un posición de carta válida.")
                    pos_tirar=int(input("¿Qué carta?, Escriba la posición de la carta: "))-1
                
                if (usuario_tipo[pos_tirar] != "+2") and (usuario_tipo[pos_tirar] != "+4"):
                    print("No puede tirar esa carta.")
                    
                else:
                    if (usuario_tipo[pos_tirar] == "+2"):
                        carta_medio(pos_tirar, pozo, usuario_color, usuario_tipo)
                        eliminar_cartas(pos_tirar, usuario_color, usuario_tipo)
                        confirma_accion = 0
                        sumarcartas+=2
                    else:
                        validar_tirada(pos_tirar, usuario_color, usuario_tipo, pozo, colores, tipos, matriz_mazo, sumarcartas)
                        confirma_accion = 0
                        sumarcartas+=4
                        
            else:
                agarrar_cartas(matriz_mazo, usuario_color, usuario_tipo, pozo, colores, tipos, 0, sumarcartas)
                confirma_accion = 0
                sumarcartas=0
                confirma_robar=0
                
    print("\nPozo:")
    printpozo(pozo)
    
    if (len(pc_tipo) == 0) or (len(usuario_tipo) == 0):
        if modo == "P":
            imprimir_blanco()
            puntos_de_la_maquina, puntos_del_usuario = carga_puntuacion(puntos_del_usuario, puntos_de_la_maquina, usuario_tipo, pc_tipo)
            print("PUNTOS DEL USUARIO")
            print(puntos_del_usuario)
            print("PUNTOS DE LA MAQUINA")
            print(puntos_de_la_maquina)
            if puntos_del_usuario > 500 or puntos_de_la_maquina > 500:
                break
            matriz_mazo, pc_color, pc_tipo, usuario_color, usuario_tipo, pozo, sumarcartas, saltar_turno, confirma_robar, posicion = inicializar_0(colores, tipos) 
        else:
            break
        
    if sumarcartas==0 or confirma_robar==0:
        if saltar_turno==False:
            if validar_uno(pc_tipo, pc_color, pozo, 1):
                print('-cpu: "UNO"')
            print("\nTurno de La Máquina")
            cantidad_cartas_cpu=len(pc_tipo)
            confirma_tiro = tirar_cartas_cpu(pc_tipo, pc_color, usuario_tipo, pozo, matriz_mazo, colores, tipos, sumarcartas)
            
            if confirma_tiro==1:
                if pozo[1]=="+2":
                    sumarcartas+=2
                    confirma_robar=1
                    confirma_tiro=0
                if pozo[1]=="+4":
                    sumarcartas+=4
                    confirma_tiro=0
                    confirma_robar=1
                if pozo[1]=="X":
                    saltar_turno=True
                    confirma_tiro=0
        else:
            imprimir_blanco()
            print("Se cancelo el turno de la maquina por carta X.")
            saltar_turno=False
    else:
        if ("+4" in pc_tipo):
            posicion = pc_tipo.index("+4")
            color_nuevo = elegir_color_cpu(pc_color, colores)
            carta_medio(posicion, pozo, pc_color, pc_tipo, color_nuevo)
            eliminar_cartas(posicion, pc_color, pc_tipo)
            sumarcartas+=4
                
        elif ("+2" in pc_tipo):
            posicion = pc_tipo.index("+2")
            carta_medio(posicion, pozo, pc_color, pc_tipo)
            eliminar_cartas(posicion, pc_color, pc_tipo)
            sumarcartas+=2
            
        else:
            agarrar_cartas(matriz_mazo, pc_color, pc_tipo, pozo, colores, tipos, 1, sumarcartas)
            sumarcartas=0
            confirma_robar=0

    imprimir_blanco()
    print("Pozo:")
    printpozo(pozo)
    imprimir_blanco()
    if cantidad_cartas_cpu < len(pc_tipo):
        print("\nLa Máquina tiro una carta")
        print("\nA la pc le quedan", len(pc_tipo), "cartas")
    elif cantidad_cartas_cpu > len(pc_tipo):
        print("\nLa Máquina agarro cartas")
        print("\nA la pc le quedan", len(pc_tipo), "cartas")
    
imprimir_blanco()
if modo == "P":
    if puntos_de_la_maquina > 500:
        print("\nTermino la partida, usted ganó")
    else:
        print("\nTermino la partida, ganó la cpu")
else:
    if (len(pc_tipo) == 0):
        print("\nTermino la partida, ganó la cpu")
    else:
        print("\nTermino la partida, usted ganó")

#Importar bibliotecas
import pygame

pygame.init()



# Area para funciones 


#Funcion de matriz


#La matriz sera creada con cada subconjuto lleno de ceros, pero sientete libre de cambiar el 0 por otro valor, como ""
#Cambie el orden de donde se colocan las funciones, ya que de lo contrario estas quedan indefinidas

def generador_matriz():
    matriz = []
    for y in range(17):
        matriz.append([])
        for x in range(26):
            matriz_subgrupo = matriz[y]
            matriz_subgrupo.append(0) #Este es el relleno de todos los elementos
    return matriz


# Clases


class Editor():
    # Atributos
    matriz = generador_matriz() #Matriz
    creador = ""
    estado_programa = ""
    estilo_imagen = ""
    #Falta agregar metodos

    def __init__(self, matriz, creador, estado_programa, estilo_imagen):
        self.matriz = matriz
        self.creador = creador
        self.estado_programa = "Creado"
        estilo_imagen = estilo_imagen

    def estado_en_ejecucion(self):
        if self.estado_programa == "Creado":
            pass

        elif self.estado_programa == "En proceso":
            pass

        elif self.estado_programa == "Terminado":
            pass
    
    def modificar_matriz(self, localizacion, valor): #Cambia un valor de la matriz
        x, y = localizacion
        self.matriz[y][x] = valor



class pincel:
    brocha = "brocha"
    borrador = False
    zoom_in = False
    zoom_out = False
    def __init__(self, brocha, borrador, zoom_in, zoom_out):
        self.brocha = brocha
        self.borrador =  borrador
        self.zoom_in = zoom_in
        self.zoom_out = zoom_out

    def interruptor_borrar(self):
        self.borrador = not self.borrador
        if self.borrador == False:
            brocha = "Brocha"
        else:
            brocha = "Borrador"

    def cambio_brocha(self):
        pass

# Area variables
tamaño_cuadros = 32 #Pixeles c/u
comienzo_dibujar_cuadros = 32 * 3 #Lugar donde se empiezan a generar los cuadros
rect_raton = pygame.Rect(0,0,10,10)
rect_raton.centerx = 400 #Cuadro que seguira al cursor

rect1 = pygame.Rect(0,0,tamaño_cuadros,tamaño_cuadros) #Rectangulo del canvas
color_rect1 = (220,220,220) #Color del rectangulo

# pygame setup
pantalla = pygame.display.set_mode((1100, 700)) #Reduje el tamaño del cuadro de (1600, 900) ---> (1100, 700), si afecta mucho la escala de tamaños aumentalo nuevamente
clock = pygame.time.Clock()

# Variable para determinar cuando se cierra la ventana
jugar = True



while jugar:

    lienzo = Editor("", "Default", "Default" )


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False


        #Esta funcion analiza en cual cuadro ocurrio la interaccion
        def analizador_de_bloques(): 
            localizacion_interaccion = []
            espacio_ventana_x = 0 #Aqui va el espacio que esta entre el lienzo y la ventana en el eje x
            espacio_ventana_y = 0 #Aqui va el espacio que esta entre el lienzo y la ventana en el eje y
            (ratonx, ratony) = pygame.mouse.get_pos()
            matriz = lienzo.matriz()
            for grupo_y in range(len(matriz)):
                for unidad_x in range(len(grupo_y)):
                    #La condicion de la siguiente linea verifica si la posicion del cursor esta en el rango efectivo del cuadro al que se quiere afectar
                    if (ratonx < ((unidad_x+1)*32) + espacio_ventana_x) and (ratonx > ((unidad_x*32) + espacio_ventana_x)) and (ratony < ((grupo_y+1)*32) + espacio_ventana_y) and (ratony > (grupo_y*32) + espacio_ventana_y ):
                        localizacion_interaccion = [unidad_x,grupo_y]
                    else:
                        continue
            return localizacion_interaccion

        #Analiza si la interacicon fue en el lienzo
        def zona_efectiva(): 
            zona_canvas_x = 0 #limite del eje x en el que se puede encontrar un cuadro, desconozco su tamaño con exactitud
            zona_canvas_y = 0 #limite del eje y en el que se puede encontrar un cuadro, desconozco su tamaño con exactitud
            (ratonx, ratony) = pygame.mouse.get_pos() 
            if ratonx > zona_canvas_x and ratony > zona_canvas_y:
                return True
            else:
                return False


        if event.type == pygame.MOUSEBUTTONDOWN:
            interaccion = zona_efectiva()
            if interaccion == True: #Comprueba si el click fue en el lienzo
                lugar_afectado = analizador_de_bloques()
                lienzo.modificar_matriz(analizador_de_bloques, )#Falta agregar codigo



    # Refrescar la pantalla por cada frame para quitar el frame anterior
    pantalla.fill("white")

    # Logica
    posicion_raton = pygame.mouse.get_pos()
    rect_raton.center = posicion_raton #colocar el Rectangulo para el raton encima del raton


    #La idea es que se cargue solo una vez al inicio,luego cuando detecte el mouse,hara que se vuelva a cargar si fuese que se selecciono un color
    
    #Generador de cuadros

    for i in range(26):     #Numero de cuadros en el eje x
        for j in range(17):     # Numero de cuadros en el ejey
            if i == 2 and j == 3:   #Porque esta condicion?
                # parametros del draw.rect: superficie,color,(posicion  )
                pygame.draw.rect(pantalla,(220,220,220),(tamaño_cuadros*i+comienzo_dibujar_cuadros,tamaño_cuadros*j+comienzo_dibujar_cuadros,tamaño_cuadros,tamaño_cuadros))
            else:
                pygame.draw.rect(pantalla,(220,220,220),(tamaño_cuadros*i+comienzo_dibujar_cuadros,tamaño_cuadros*j+comienzo_dibujar_cuadros,tamaño_cuadros,tamaño_cuadros),3)

    
    pygame.draw.rect(pantalla,(0,255,255),rect_raton,3)#Se cambia al final para que el color sea blanco,es para la deteccion de colision entre el rato y un cuadro
    pygame.draw.rect(pantalla,color_rect1,rect1)#Se cambia al final para que el color sea blanco,es para la deteccion de colision entre el rato y un cuadro

    # Colocar en la pantalla el renderizado
    pygame.display.flip()    


    # Para fijar el juego a 60 fps
    clock.tick(60) 


pygame.quit()


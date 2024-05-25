#Importar bibliotecas
import pygame

pygame.init()

#Sa

# Area para funciones 


#Funcion de matriz


#La matriz sera creada con cada subconjuto lleno de ceros, pero sientete libre de cambiar el 0 por otro valor, como ""
#Cambie el orden de donde se colocan las funciones, ya que de lo contrario estas quedan indefinidas

def generador_matriz():
    matriz = []
    for y in range(17):
        matriz.append([])
        for x in range(26):
            matriz_subgrupo = matriz[x]
            matriz_subgrupo.append(0) #Este es el relleno de todos los elementos
    return matriz


# Clases

class Editor():
    # Atributos
    matriz_imagen = generador_matriz() #Matriz
    creador = ""
    estado_programa = ""
    #Falta agregar metodos

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False


        #Detecta si hay colision con un cuadro Y si se realizo un click con el mouse
        #Sin embargo, no puedo realizar cambios de como funciona dicha colision por la line de codigo ya creada con dicha funcion en la linea 84
        if event.type == pygame.MOUSEBUTTONDOWN and rect_raton.colliderect(rect1):
        #    Falta agregar el resto


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

    
    if rect_raton.colliderect(rect1):
        color_rect1 = (0,220,220)

    pygame.draw.rect(pantalla,(0,255,255),rect_raton,3)#Se cambia al final para que el color sea blanco,es para la deteccion de colision entre el rato y un cuadro
    pygame.draw.rect(pantalla,color_rect1,rect1)#Se cambia al final para que el color sea blanco,es para la deteccion de colision entre el rato y un cuadro

    # Colocar en la pantalla el renderizado
    pygame.display.flip()    


    # Para fijar el juego a 60 fps
    clock.tick(60) 


pygame.quit()
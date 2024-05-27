#Importar bibliotecas
import pygame

pygame.init()




# Area variables globales
tamaño_cuadros = 32 #Pixeles c/u
comienzo_dibujar_cuadros = tamaño_cuadros * 3 #Lugar donde se empiezan a generar los cuadros
rect_raton = pygame.Rect(0,0,10,10)

gris = (220,220,220)

estado = 'pintar en lienzo' #Trabajarlo por estados para mas comodidad



# Area para funciones 

#Funcion de matriz

#La matriz sera creada con cada subconjuto lleno de ceros, pero sientete libre de cambiar el 0 por otro valor, como ""
#Cambie el orden de donde se colocan las funciones, ya que de lo contrario estas quedan indefinidas

def generador_matriz():
    matriz = []
    matriz_rects=[]
    for fila in range(0,17):
        matriz.append([])
        for columna in range(0,26):
            matriz[fila].append(0) #Este es el relleno de todos los elementos de la matriz de 0
            rect = pygame.Rect((tamaño_cuadros+0.2)*fila+comienzo_dibujar_cuadros,
                               (tamaño_cuadros+0.1)*columna+comienzo_dibujar_cuadros, 
                               tamaño_cuadros*0.92, 
                               tamaño_cuadros*0.92) 
            matriz_rects.append(rect) #Rectangulos del canvas
    return matriz,matriz_rects



# Clases

class Editor():
    # Atributos
    matriz,matriz_rects = generador_matriz() #Matriz
    creador = ""
    estado_programa = ""
    estilo_imagen = ""
    #Falta agregar metodos

    def __init__(self, creador, estado_programa, estilo_imagen):
        self.creador = creador
        self.estado_programa = "Creado"
        self.estilo_imagen = estilo_imagen

    def estado_en_ejecucion(self):
        if self.estado_programa == "Creado":
            pass

        elif self.estado_programa == "En proceso":
            pass

        elif self.estado_programa == "Terminado":
            pass
    
    def editar_imagen(self, localizacion, valor): #Cambia un valor de la matriz
        x, y = localizacion
        self.matriz[y][x] = valor
###
#
#
#
# Clases van con nombre mayuscula
#
#
#
##
class Pincel:
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

class Color:
    imagen=''
    tamaño_imagen=0
    id=''
    posicion_x=0
    posicion_y=0
    def __init__(self, imagen, id, tamaño_imagen,posicion_x,posicion_y):
        self.imagen = pygame.image.load(imagen)
        self.id = id
        self.tamaño_imagen = tamaño_imagen
        self.imagen = pygame.transform.scale(self.imagen,(tamaño_imagen*tamaño_cuadros,tamaño_imagen*tamaño_cuadros))
        self.rect = self.imagen.get_rect()
        self.posicion_x = posicion_x * tamaño_cuadros
        self.posicion_y = posicion_y * tamaño_cuadros

    def generar_cuadro(self):
        pantalla.blit(self.imagen,(self.posicion_x,self.posicion_y ))
        
        



# pygame setup
pantalla = pygame.display.set_mode((1100, 700)) #Reduje el tamaño del cuadro de (1600, 900) ---> (1100, 700), si afecta mucho la escala de tamaños aumentalo nuevamente
clock = pygame.time.Clock()

# Variable para determinar cuando se cierra la ventana
jugar = True
# Iniciar objetos
lienzo = Editor("", "Default", "Default")

colores = [['amarillo',1,2,1,2 ],['celeste',1,2,1,3],['gris',1,2,1,4],['morado',1,2,1,5],['naranja',1,2,1,6],['rojo',1,2,1,7]
           ,['rosado',1,2,1,8],['verde',1,2,1,9]]

objetos_colores=[]
for fila in colores:
    color = Color(f'colores/{fila[0]}.png',fila[1],fila[2],fila[3],fila[4]) #Colores
    objetos_colores.append(color)




while jugar:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False

        if event.type == pygame.MOUSEBUTTONDOWN: 
            for elemento in  lienzo.matriz_rects :
                    if rect_raton.colliderect(elemento):
                        pygame.draw.rect(pantalla,(0,220,220),elemento)#pinta del color(0,220,220)
                        lienzo.editar_imagen


    for elemento in objetos_colores:
        elemento.generar_cuadro()

    # Logica
    posicion_raton = pygame.mouse.get_pos()
    rect_raton.center = posicion_raton #colocar el Rectangulo para el raton encima del raton


    #La idea es que se cargue solo una vez al inicio,luego cuando detecte el mouse,hara que se vuelva a cargar si fuese que se selecciono un color
    
    #Generador de cuadros
    if estado == 'pintar en lienzo':
        pantalla.fill("white")
        print(lienzo.matriz)

        for fila in range(0, len(lienzo.matriz ) ):     #Numero de cuadros en el eje x
            for columna in range(0,len(lienzo.matriz) ):     # Numero de cuadros en el ejey
                pygame.draw.rect(pantalla,(220,220,220),(tamaño_cuadros*fila+comienzo_dibujar_cuadros,tamaño_cuadros*columna+comienzo_dibujar_cuadros,tamaño_cuadros,tamaño_cuadros),2)
       
        estado = 'siguiente'

    #pygame.draw.rect(pantalla,(0,255,255),rect_raton,3)#Se cambia al final para que el color sea blanco,es para la deteccion de colision entre el rato y un cuadro
    #pygame.draw.rect(pantalla,color_rect1,rect1,2)#Se cambia al final para que el color sea blanco,es para la deteccion de colision entre el rato y un cuadro
    # Colocar en la pantalla el renderizado
    pygame.display.flip()    


    # Para fijar el juego a 60 fps
    clock.tick(60) 


pygame.quit()
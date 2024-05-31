#Importar bibliotecas
import pygame

pygame.init()


# Area variables globales
tamaño_cuadros = 32 #Pixeles c/u
comienzo_dibujar_cuadrosx = tamaño_cuadros * 6 #Lugar donde se empiezan a generar los cuadros x
comienzo_dibujar_cuadrosy = tamaño_cuadros * 3 #Lugar donde se empiezan a generar los cuadros y 
rect_raton = pygame.Rect(0,0,5,5) #el rect que sigue al raton

fuente = pygame.font.SysFont("Calibri", 17) #Tipo de fuente para el texto

gris = (220,220,220)
gris_oscuro = (180, 180, 180)
amarillo = (255,242,0 )
celeste = (122,191,236)
grispintura = (225,225,255)
morado = (184,121,231)
naranja = (240,194,121)
rojo = (249,99,116)
rosado = (235,115,169)
verde = (115,233,145)
blanco = (255,255,255)
negro = (0,0,0)
color_seleccionado = "gris"
id_seleccionado = -1

estado = 'pintar en lienzo' #Trabajar por estados para mas comodidad

pantalla = pygame.display.set_mode((1280, 720)) #Reduje el tamaño del cuadro de (1600, 900) ---> (1100, 700), si afecta mucho la escala de tamaños aumentalo nuevamente
clock = pygame.time.Clock()

jugar = True # Variable para determinar cuando se cierra la ventana

# Area para funciones 

def generador_matriz():
    matriz = []
    matriz_rects=[]
    for fila in range(0,10):
        matriz.append([])
        matriz_rects.append([])
        for columna in range(0,10):
            matriz[fila].append(0) #Este es el relleno de todos los elementos de la matriz de 0
            rect = pygame.Rect((tamaño_cuadros+0.2)*fila+comienzo_dibujar_cuadrosx,
                               (tamaño_cuadros+0.1)*columna+comienzo_dibujar_cuadrosy, 
                               tamaño_cuadros*0.92, 
                               tamaño_cuadros*0.92) 
            matriz_rects[fila].append(rect) #Rectangulos del canvas
    return matriz,matriz_rects


    

# Clases

class Editor():
    # Atributos
    matriz,matriz_rects = generador_matriz() #Matriz
    creador = ""
    estado_programa = ""
    estilo_imagen = ""
    archivo_en_uso = ""
    nombre_archivo = ""
    numero_de_archivos = 1

    #Falta agregar metodos

    def __init__(self, creador, estado_programa, estilo_imagen, archivo_en_uso, nombre_archivo, numero_de_archivos):
        self.creador = creador
        self.estado_programa = "Creado"
        self.estilo_imagen = estilo_imagen
        self.archivo_en_uso = archivo_en_uso
        self.nombre_archivo = "Epitome_del_arte_"
        self.numero_de_archivos = numero_de_archivos


    def estado_en_ejecucion(self):
        if self.estado_programa == "Creado":
            pass

        elif self.estado_programa == "En proceso":
            pass

        elif self.estado_programa == "Terminado":
            pass

    def crear_archivos(self):

        nombre = (self.nombre_archivo + str(self.numero_de_archivos))+".txt" #Crea un nombre nuevo con los parametros guardador y un nuevo nombre
        open(nombre, 'w') #Crea un archivo
        self.archivo_en_uso = nombre #Cambia el nombre guardado
    
    def guardar_archivo(self):
        if not self.archivo_en_uso == "": #Verifica si ya se modifico que nombre original con la creacion de un archivo de texto
            with open(self.archivo_en_uso, 'w') as old_archivo:
                pass
            self.archivo_en_uso.write(self.matriz)

    #Lo planeado es que en la interfaz se elija el archivo que se quiere editar a base de numeros, para asi acceder a el
    #Ejemplor, el archivo 2 seria "Epitome_del_arte_2.txt", solo cambiando el numero que acompaña al nombre por defecto para acceder a dicho archivo

    def restar_guardados(self):
        if self.numero_de_archivos > 1: #Comprueba que el archivo no sea igual a 0
            self.numero_de_archivos -= 1 #Suma 1 al archivo que se quiere acceder

    def cargar_archivo(self): #Incompleto
        nombre = (self.nombre_archivo + str(self.numero_de_archivos))+".txt"

    def sumar_guardados(self):
        self.numero_de_archivos += 1 #Suma 1 al archivo que se quiere acceder

    def editar_imagen(self, x, y, valorid): #Cambia un valor de la matriz
        self.matriz[x][y] = valorid




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

class Color: #Genera los colores junto con su colision correspondiente con el raton
    imagen = ''
    tamaño_imagen=0
    id = ''
    posicion_x = 0
    posicion_y = 0
    rect = 0
    color = ""

    def __init__(self, imagen, id, tamaño_imagen,posicion_x,posicion_y,color):#Inicializador de la clase
        self.imagen = pygame.image.load(imagen)
        self.id = id
        self.tamaño_imagen = tamaño_imagen*tamaño_cuadros
        self.imagen = pygame.transform.scale(self.imagen,(tamaño_imagen*tamaño_cuadros,tamaño_imagen*tamaño_cuadros))
        self.posicion_x = posicion_x * tamaño_cuadros
        self.posicion_y = posicion_y * tamaño_cuadros
        self.rect = pygame.Rect( self.posicion_x  , self.posicion_y, self.tamaño_imagen, self.tamaño_imagen  )
        self.color = color

    def generar_cuadro(self):#Pinta en pantalla el cuadro de color
        pantalla.blit(self.imagen,(self.posicion_x,self.posicion_y ))
    
    def devolver_rect(self):#devuelve el rect del cuadro de color
        return self.rect

# Iniciar objetos
lienzo = Editor("", "Default", "Default", "", "Epitome_del_arte_", 0)

#Color parametros: nombre,id,tamanio,posicion x(se multiiplica por el tamanio del cuadro), posicion y
colores = [['amarillo',2,2,1,2 ],
           ['celeste',1,2,35,2],
           ['gris',8,2,35,4],
           ['morado',7,2,35,6],
           ['naranja',3,2,35,8],
           ['rojo',4,2,35,10],
           ['rosado',5,2,1,4],
           ['verde',6,2,1,6],
           ['blanco',0,2,1,8],
           ['negro',9,2,1,10]]

objetos_colores=[]
for fila in colores:#cargar los colroes en pantalla
    color = Color(f'colores/{fila[0]}.png',fila[1],fila[2],fila[3],fila[4],fila[0]) #Colores objetos
    objetos_colores.append(color)

#Localizacion y medidas de los botones
boton_guardar_archivo =  225,510,120,70
boton_archivo_nuevo =  375,510,120,70


cuadro_interfaz = 550, 96, 200, 100 
cuadro_resta = 560, 106, 20, 20
cuadro_carga = 590, 106, 100, 20
cuadros_suma = 700, 106, 20, 20


#Texto y fuente para los botones
texto_guardar = fuente.render("Guardar archivo", True, blanco)
texto_nuevo = fuente.render("Nuevo archivo", True, blanco)
texto_resta = fuente.render("-", True, blanco)
texto_carga = fuente.render("Cargar Archivo", True, blanco)
texto_suma = fuente.render("+", True, blanco)
texto_archivo_a_cargar = fuente.render("", True, blanco)

while jugar:

    #Rectangulos de los botones de guardar, crear un nuevo archivo y cargar
    boton_guardar =  pygame.draw.rect(pantalla,gris_oscuro, boton_guardar_archivo )
    boton_nuevo = pygame.draw.rect(pantalla,gris_oscuro, boton_archivo_nuevo )

    #Botones para cargar archivos
    interfaz_guardado = pygame.draw.rect(pantalla, gris, cuadro_interfaz)
    boton_resta = pygame.draw.rect(pantalla, gris_oscuro, cuadro_resta)
    boton_carga = pygame.draw.rect(pantalla, gris_oscuro, cuadro_carga)
    boton_suma =  pygame.draw.rect(pantalla, gris_oscuro, cuadros_suma)

    #Implementacion del texto en los botones
    pantalla.blit(texto_guardar,( 232,537 ))
    pantalla.blit(texto_nuevo, ( 385, 537 ))
    pantalla.blit(texto_resta,(565, 106))
    pantalla.blit(texto_carga,(590, 106))
    pantalla.blit(texto_suma,(705, 106))


    #Logica
    posicion_raton = pygame.mouse.get_pos()
    rect_raton.center = posicion_raton #colocar el Rectangulo para el raton encima del raton
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False

        if event.type == pygame.MOUSEBUTTONDOWN: 
            for numfila,fila in enumerate(lienzo.matriz_rects) :
                for numcolumna,columna in enumerate(fila):
                    if rect_raton.colliderect(columna):
                        pygame.draw.rect(pantalla,eval(color_seleccionado),columna)#pinta del color el cuadro que colisiona con el click del raton
                        lienzo.editar_imagen(numcolumna,numfila,id_seleccionado)#modifica la matriz de 0 con el id correspodiente al color
                        print(lienzo.matriz)#ver matriz
            for elemento in objetos_colores:# seleccion de color con raton
                if rect_raton.colliderect( elemento.devolver_rect() ): #si se selecciona
                    color_seleccionado = elemento.color #Variable global color_seleccionado cambia al color que se selecciono,ver lista objetos colores
                    id_seleccionado = elemento.id #Variable global id_seleccionado cambia al id del color que se selecciono
        
            #Interacciones con los botones de guardar, cargar y crear

            if boton_guardar.collidepoint(posicion_raton):
                Editor.guardar_archivo()
            if boton_nuevo.collidepoint(posicion_raton):
                Editor.crear_archivos()
            if boton_resta.collidepoint(posicion_raton):
                Editor.restar_guardados()
            if boton_carga.collidepoint(posicion_raton):
                Editor.cargar_archivo()
            if boton_suma.collidepoint(posicion_raton):
                Editor.sumar_guardados()



    
    for elemento in objetos_colores: #generar cuadro de colores
        elemento.generar_cuadro()


    if estado == 'pintar en lienzo':    #Generador de cuadros de matriz en pantalla
        pantalla.fill((245,245,245))
        print(lienzo.matriz)
        for fila in range(0, len( lienzo.matriz ) ):     #Numero de cuadros en el eje x
            for columna in range( 0, len( lienzo.matriz[0] ) ):     # Numero de cuadros en el eje y
                pygame.draw.rect(pantalla,
                                 gris,
                                 (tamaño_cuadros*fila+comienzo_dibujar_cuadrosx,tamaño_cuadros*columna+comienzo_dibujar_cuadrosy,tamaño_cuadros,tamaño_cuadros),
                                 2)
        estado = 'siguiente'

    # Colocar en la pantalla el renderizado
    pygame.display.flip()    

    # Para fijar el juego a 60 fps
    clock.tick(60) 

pygame.quit()
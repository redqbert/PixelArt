#Importar bibliotecas
import pygame

pygame.init()

# Area variables globales
tamaño_cuadros = 16 #Pixeles c/u
comienzo_dibujar_cuadrosx = tamaño_cuadros * 6 #Lugar donde se empiezan a generar los cuadros x
comienzo_dibujar_cuadrosy = tamaño_cuadros * 3 #Lugar donde se empiezan a generar los cuadros y 
rect_raton = pygame.Rect(0,0,5,5) #el rect que sigue al raton

fuente = pygame.font.SysFont("Calibri", 17) #Tipo de fuente para el texto

gris = (220,220,220)
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
color_seleccionado = "blanco"
id_seleccionado = 0

estado = 'pintar en lienzo' #Trabajar por estados para mas comodidad

pantalla = pygame.display.set_mode((1280, 720)) 
clock = pygame.time.Clock()

jugar = True # Variable para determinar cuando se cierra la ventana

# Area para funciones 

def generador_matriz():
    matriz = []
    matriz_rects=[]
    for fila in range(0,30):
        matriz.append([])
        matriz_rects.append([])
        for columna in range(0,30):
            matriz[fila].append(0) #Este es el relleno de todos los elementos de la matriz de 0
            rect = pygame.Rect((tamaño_cuadros)*fila+comienzo_dibujar_cuadrosx,
                               (tamaño_cuadros)*columna+comienzo_dibujar_cuadrosy, 
                               tamaño_cuadros, 
                               tamaño_cuadros) 
            matriz_rects[fila].append(rect) #rectangulos del canvas
    return matriz,matriz_rects

#se pasa de filas a columnas 
def trasponer_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    # crear matriz traspuesta vacía
    matriz_transpuesta = [[0 for _ in range(filas)] for _ in range(columnas)]

    # recorrer matriz original y copiar elementos a la traspuesta
    for i in range(filas):
        for j in range(columnas):
            matriz_transpuesta[j][i] = matriz[i][j]

    return matriz_transpuesta

#Rotar izquierda la matriz
def trasponer_con_cambio_orden(matriz):
  filas = len(matriz)
  columnas = len(matriz[0])
  # crear una nueva matriz
  matriz_transpuesta = [[0 for _ in range(filas)] for _ in range(columnas)]
  # recorrer matriz original en orden inverso de columnas
  for i in range(columnas - 1, -1, -1):
    # recorrer las filas de la columna actual
    for j in range(filas):
      matriz_transpuesta[filas - 1 - j][i] = matriz[j][i]

  return matriz_transpuesta

def alto_contraste_matriz(matriz):
  for fila in matriz:
    for i in range(len(fila)):
      #si el valor se encuentra entre 0 y 4 entonces se cambia por 1
      if 0 <= fila[i] <= 4:
        fila[i] = 1
      #si el valor esta entre 5 y 9 se cambiar a 9
      elif 5 <= fila[i] <= 9:
        fila[i] = 9
  return matriz

#darle vuelta a los valores del id
def revertir_matriz(matriz):

  matriz_revertida = []
  for row in matriz:
    new_row = []
    for value in row:
      new_row.append(9 - value)
    matriz_revertida.append(new_row)
  return matriz_revertida


# reorganizar columnas de la matriz
def reflejo_matriz_hor(matriz):
    matriz_reorganizada = []
    num_columnas = len(matriz[0])
    
    for fila in matriz:
        nueva_fila = [fila[i] for i in range(num_columnas - 1, -1, -1)]
        matriz_reorganizada.append(nueva_fila)
    
    return matriz_reorganizada


# invierte las filas de la matriz
def reflejo_matriz_ver(matriz):
    return matriz[::-1]



# Clases

class Editor():
    # Atributos
    matriz,matriz_rects = generador_matriz() #Matriz
    creador = ""
    estado_programa = ""
    estilo_imagen = ""
    archivo_en_uso = ""
    nombre_archivo = ""
    numero_de_archivos = 0
    ascii = 0
    #Falta agregar metodos
    def __init__(self, creador, estado_programa, estilo_imagen, archivo_en_uso, nombre_archivo, numero_de_archivos,ascii):
        self.creador = creador
        self.estado_programa = estado_programa
        self.estilo_imagen = estilo_imagen
        self.archivo_en_uso = archivo_en_uso
        self.nombre_archivo = nombre_archivo
        self.numero_de_archivos = 0
        self.ascii = ascii

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
        self.numero_de_archivos += 1 
    
    def guardar_archivo(self):
        nombre = self.archivo_en_uso
        # Convierte la matriz a una cadena de texto
        matriz_str = ""
        for fila in self.matriz:
            for elemento in fila:
                matriz_str += str(elemento) + " "
            matriz_str += "\n"
        with open(nombre, 'w') as archivo:
            archivo.write(matriz_str)

    def cargar_matriz(self):
        # abrir archivo
        with open("Epitome_del_arte_0.txt", "r") as archivo:
            datos_matriz = archivo.read()
        # convertir a matriz
        filas = datos_matriz.split("\n")
        matriz_cargada = []
        for fila in filas:
            columna_str = fila.split(" ")
            columna_num = []
            for elemento in columna_str:
                # quitarse errores de encima
                try:
                    elemento_num = int(elemento)
                except ValueError:
                    elemento_num = 0  # para casos en los que hay error se pone un 0
                columna_num.append(elemento_num)
            matriz_cargada.append(columna_num)
        # actualizar la matriz del objeto
        self.matriz = matriz_cargada

    def editar_imagen(self, x, y, valorid): #Cambia un valor de la matriz
        self.matriz[x][y] = valorid

    def cargar_imagen(self):
        pantalla.fill((245,245,245))
        for fila in range(0, len( self.matriz )-1 ):     #Numero de cuadros en el eje x
            for columna in range( 0, len( self.matriz[0] )-1 ):     # Numero de cuadros en el eje y
                for elemento in colores:
                    if self.matriz[columna][fila] == elemento[1]:#elemento 1 es id
                        pygame.draw.rect(pantalla,
                                        eval(elemento[0]),#nombre del color
                                        (tamaño_cuadros*fila+comienzo_dibujar_cuadrosx,tamaño_cuadros*columna+comienzo_dibujar_cuadrosy,tamaño_cuadros,tamaño_cuadros)
                                        )
                    else:
                        pygame.draw.rect(pantalla,
                                 gris,
                                 (tamaño_cuadros*fila+comienzo_dibujar_cuadrosx,tamaño_cuadros*columna+comienzo_dibujar_cuadrosy,tamaño_cuadros,tamaño_cuadros),
                                 1)
        
    def mostrar_matriz(self):#mostrar la matriz numerica en pantalla
        pantalla.fill((245,245,245))
        for fila in range(0, len( self.matriz )-1 ):     #Numero de cuadros en el eje x
            for columna in range( 0, len( self.matriz[0] )-1 ):     # Numero de cuadros en el eje y
                for elemento in self.ascii:
                        if self.matriz[columna][fila] == elemento[2]:
                            pantalla.blit(elemento[3],
                                        (fila*tamaño_cuadros+comienzo_dibujar_cuadrosx,columna*tamaño_cuadros+comienzo_dibujar_cuadrosy,tamaño_cuadros,tamaño_cuadros),
                                        elemento[4])

    def ascii_art(self):
        pantalla.fill((245,245,245))
        for fila in range(0, len( self.matriz )-1 ):     #Numero de cuadros en el eje x
            for columna in range( 0, len( self.matriz[0] )-1 ):     # Numero de cuadros en el eje y
                for elemento in self.ascii:
                        if self.matriz[columna][fila] == elemento[2]:
                            pantalla.blit(elemento[0],
                                        (fila*tamaño_cuadros+comienzo_dibujar_cuadrosx,columna*tamaño_cuadros+comienzo_dibujar_cuadrosy,tamaño_cuadros,tamaño_cuadros),
                                        elemento[1])
                            
    def rotar_derecha_matriz(self):
        pantalla.fill((245,245,245))
        self.matriz = trasponer_matriz(self.matriz)
        self.cargar_imagen()
                
    def rotar_izquierda_matriz(self):
        pantalla.fill((245,245,245))
        self.matriz = trasponer_con_cambio_orden(self.matriz)
        print(self.matriz)
        self.cargar_imagen()
    
    def alto_contraste(self):
        pantalla.fill((245,245,245))
        self.matriz = alto_contraste_matriz(self.matriz)
        self.mostrar_matriz()

    def negativo(self):
        pantalla.fill((245,245,245))
        self.matriz = revertir_matriz(self.matriz)
        self.cargar_imagen()
    
    def reflejo_hor(self):
        pantalla.fill((245,245,245))
        self.matriz = reflejo_matriz_hor(self.matriz)
        self.cargar_imagen()

    def reflejo_ver(self):
        pantalla.fill((245,245,245))
        print("hola mundo")
        self.matriz = reflejo_matriz_ver(self.matriz)
        self.cargar_imagen()


            
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

class Iconos:
    imagen = ""
    tamaño_iconos = 0
    posicionx = 0
    posiciony = 0
    rect_icono = 0
    funcion_realizar = ""
    def __init__(self, imagen, posicionx, posiciony,tamaño_imagen,funcion):
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen,(tamaño_imagen,tamaño_imagen ) )
        self.tamaño_iconos = tamaño_imagen 
        self.posicionx = posicionx 
        self.posiciony = posiciony 
        self.rect_icono = pygame.Rect( self.posicionx , self.posiciony, self.tamaño_iconos, self.tamaño_iconos  )
        self.funcion = funcion

    def mostrar_icono(self):
        pantalla.blit(self.imagen,
                      (self.posicionx,self.posiciony),
                    )
   

# Iniciar objetos

ascii_art=[]

for numero in range(0,10):
    imagenasciiart = pygame.image.load ( f"asciiart/{numero}.png" )
    imagenasciiart = pygame.transform.scale( imagenasciiart , ( tamaño_cuadros , tamaño_cuadros ) )
    imagenasciiart_rect =  imagenasciiart.get_rect()

    imagennumerica = pygame.image.load ( f"numeros/{numero}.png" )
    imagennumerica = pygame.transform.scale( imagennumerica , ( tamaño_cuadros , tamaño_cuadros ) )
    imagennumerica_rect = imagennumerica.get_rect()

    imagen = ( imagenasciiart , imagenasciiart_rect,numero,imagennumerica,imagennumerica_rect )
    ascii_art.append ( imagen )

lienzo = Editor("", "Default", "Default", "", "Epitome_del_arte_", 0,ascii_art)

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


# imagen,posicionx,posisicony,tamaño,funcion
iconos=[
    ["iconos/rotar_izq.png",20,250,40,"rotar_izq"],
    ["iconos/rotar_der.png",20,300,40,"rotar_der"],
    ['numeros/0.png',20,350,40,'matriz_num'],
    ['asciiart/9.png',20,400,40,'matriz_ascii'],
    ['iconos/contraste.png',20,450,40,'alto_contraste'],
    ['iconos/negativo.jpg',20,500,40,'negative'],
    ["iconos/borrador.png",20,550,40,"borrar"],
    ["iconos/ref_hor.png",20,600,40,"ref_hor"],
    ["iconos/ref_vert.png",20,650,40,"ref_vert"],
]

iconos_objetos = []
for fila in iconos:
    icono = Iconos(fila[0],fila[1],fila[2],fila[3],fila[4])
    iconos_objetos.append(icono)

boton_guardar_archivo =  150,510,120,70
boton_archivo_nuevo =  300,510,120,70
boton_cargar_archivo =  450,510,120,70

#Texto y fuente para los botones
texto_guardar = fuente.render("Guardar archivo", True, blanco)
texto_nuevo = fuente.render("Nuevo archivo", True, blanco)
texto_cargar = fuente.render("Cargar archivo", True, blanco)

while jugar:

    #Rectangulos de los botones de guardar, crear un nuevo archivo y cargar
    boton_guardar =  pygame.draw.rect(pantalla,gris, boton_guardar_archivo )
    boton_nuevo = pygame.draw.rect(pantalla,gris, boton_archivo_nuevo )
    boton_cargar = pygame.draw.rect(pantalla,gris, boton_cargar_archivo )

    #Implementacion del texto en los botones
    pantalla.blit(texto_guardar,( 157,537 ))
    pantalla.blit(texto_nuevo, ( 310, 537 ))
    pantalla.blit(texto_cargar,( 460,537 ))

    #Logica
    posicion_raton = pygame.mouse.get_pos()
    rect_raton.center = posicion_raton #colocar el Rectangulo para el raton encima del raton
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False

        if event.type == pygame.MOUSEBUTTONDOWN: 
            #Detecta colsion con algun cuadro de la matriz,luego guarda en la matriz el cuadro modificado con el respectivo id del color
            for numfila,fila in enumerate(lienzo.matriz_rects) :
                for numcolumna,columna in enumerate(fila):
                    if rect_raton.colliderect(columna):
                        pygame.draw.rect(pantalla,eval(color_seleccionado),columna)#pinta del color el cuadro que colisiona con el click del raton
                        lienzo.editar_imagen(numcolumna,numfila,id_seleccionado)#modifica la matriz de 0 con el id correspodiente al color
                        print(lienzo.matriz)#ver matriz
                        estado = 'pintar en lienzo'
            for elemento in objetos_colores:# Colision para la seleccion de color con raton
                if rect_raton.colliderect( elemento.devolver_rect() ): #si se selecciona
                    color_seleccionado = elemento.color #Variable global color_seleccionado cambia al color que se selecciono,ver lista objetos colores
                    id_seleccionado = elemento.id #Variable global id_seleccionado cambia al id del color que se selecciono
            #parte de funciones de botones
            for elemento in iconos_objetos:
                if rect_raton.colliderect(elemento.rect_icono):
                    if elemento.funcion == "rotar_izq":
                        lienzo.rotar_izquierda_matriz()
                    elif elemento.funcion == "rotar_der":
                        lienzo.rotar_derecha_matriz()
                    elif elemento.funcion == 'matriz_num':
                        lienzo.mostrar_matriz()
                    elif elemento.funcion == 'matriz_ascii':
                        lienzo.ascii_art()
                    elif elemento.funcion == "alto_contraste":
                        lienzo.alto_contraste()
                    elif elemento.funcion == "negative":
                        lienzo.negativo()
                    elif elemento.funcion == "borrar":
                        color_seleccionado = "blanco"
                        id_seleccionado = 0
                    elif elemento.funcion == "ref_hor":
                        lienzo.reflejo_hor()
                    elif elemento.funcion == "ref_vert":
                        lienzo.reflejo_ver()
                    

            #Interacciones con los botones de guardar, cargar y crear

            if boton_guardar.collidepoint(posicion_raton):
                lienzo.mostrar_matriz()
            if boton_nuevo.collidepoint(posicion_raton):
                lienzo.crear_archivos()
            if boton_cargar.collidepoint(posicion_raton):
                estado = 'cargar_imagen'
                lienzo.cargar_matriz()

    #generar objetos
    for elemento in objetos_colores: 
        elemento.generar_cuadro()

    for elemento in iconos_objetos:
        elemento.mostrar_icono()
    
    #Generador de cuadros de matriz en pantalla
    if estado == 'pintar en lienzo':    
        lienzo.cargar_imagen()
        estado = ''

    elif estado == 'cargar_imagen':
        lienzo.cargar_imagen()
        estado = ''

    # Colocar en la pantalla el renderizado
    pygame.display.flip()    

    # Para fijar el juego a 60 fps
    clock.tick(60) 

pygame.quit()
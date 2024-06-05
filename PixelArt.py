#Importar bibliotecas
import pygame
import pygame_gui
pygame.init()

# Area variables globales
tamaño_cuadros = 7 #Pixeles c/u
comienzo_dibujar_cuadrosx = tamaño_cuadros * 15 #Lugar donde se empiezan a generar los cuadros x
comienzo_dibujar_cuadrosy = tamaño_cuadros * 3 #Lugar donde se empiezan a generar los cuadros y 
rect_raton = pygame.Rect(0,0,2,2) #el rect que sigue al raton
tamaño_matriz=90
fuente = pygame.font.SysFont("Calibri", 17) #Tipo de fuente para el texto
menu=True

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

pantalla = pygame.display.set_mode((1000, 720)) 

clock = pygame.time.Clock()

jugar = True # Variable para determinar cuando se cierra la ventana


manager = pygame_gui.UIManager((1600, 900))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=manager,
                                               object_id='#main_text_entry')




# Area para funciones 

def generador_matriz():
    matriz = []
    matriz_rects=[]
    for fila in range(0,tamaño_matriz):
        matriz.append([])
        matriz_rects.append([])
        for columna in range(0,tamaño_matriz):
            matriz[fila].append(0) #Este es el relleno de todos los elementos de la matriz de 0
            rect = pygame.Rect((tamaño_cuadros)*fila+comienzo_dibujar_cuadrosx,
                               (tamaño_cuadros)*columna+comienzo_dibujar_cuadrosy, 
                               tamaño_cuadros, 
                               tamaño_cuadros) 
            matriz_rects[fila].append(rect) #rectangulos del canvas
    return matriz,matriz_rects

def actualizar_rects(matriz):
    matriz_rects=[]
    for fila in range(0,len(matriz)-1):
        matriz_rects.append([])
        for columna in range(0,len(matriz)-1):
            rect = pygame.Rect((tamaño_cuadros)*fila+comienzo_dibujar_cuadrosx,
                               (tamaño_cuadros)*columna+comienzo_dibujar_cuadrosy, 
                               tamaño_cuadros, 
                               tamaño_cuadros) 
            matriz_rects[fila].append(rect) #rectangulos del canvas
    return matriz_rects

def actualizar_imagenes():
    
    for numero in range(0,10):
        imagenasciiart = pygame.image.load ( f"asciiart/{numero}.png" )
        imagenasciiart = pygame.transform.scale( imagenasciiart , ( tamaño_cuadros , tamaño_cuadros ) )
        imagenasciiart_rect =  imagenasciiart.get_rect()

        imagennumerica = pygame.image.load ( f"numeros/{numero}.png" )
        imagennumerica = pygame.transform.scale( imagennumerica , ( tamaño_cuadros , tamaño_cuadros ) )
        imagennumerica_rect = imagennumerica.get_rect()

        imagen = ( imagenasciiart , imagenasciiart_rect,numero,imagennumerica,imagennumerica_rect )
        ascii_art.append ( imagen )


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

def convertir_columnas_a_filas(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    
    matriz_resultante = []
    for j in range(columnas - 1, -1, -1): #ir en las columnas pero hacia atras
        nueva_fila = []
        for i in range(filas):  # ir en las filas en orden normal
            nueva_fila.append(matriz[filas - i - 1][j])  # para invertir el orden de las filas
        matriz_resultante.append(nueva_fila)
    
    return matriz_resultante

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

#crea el entrador de datos
def nombre():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                
            if (evento.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                evento.ui_object_id == '#main_text_entry'):
                return evento.text
            
            manager.process_events(evento)
        
        manager.update(clock.tick(60)/1000)

        manager.draw_ui(pantalla)

        pygame.display.update()

# Clases

class Editor():
    # Atributos
    matriz,matriz_rects = generador_matriz() #Matriz
    creador = ""
    estado_programa = ""
    nombre_archivo = ""
    ascii = 0
    tamaño_cuadros=0
    #Falta agregar metodos
    def __init__(self, creador, estado_programa, nombre_archivo,ascii):
        self.creador = creador
        self.estado_programa = estado_programa
        self.nombre_archivo = nombre_archivo
        self.ascii = ascii

    def crear_archivos(self):
        nombre = (self.nombre_archivo)+".txt" #Crea un nombre nuevo con los parametros guardador y un nuevo nombre
        open(nombre, 'w') #Crea un archivo
    
    def guardar_archivo(self):
        nombre = self.nombre_archivo+".txt"
        # Convierte la matriz a una cadena de texto
        matriz_str = ""
        for fila in self.matriz:
            for elemento in fila:
                matriz_str += str(elemento) + " "
            matriz_str += "\n"
        with open(nombre, 'w') as archivo:
            archivo.write(matriz_str)

    def cargar_matriz(self):
        # Abrir archivo
        try:
            with open(self.nombre_archivo + ".txt", "r") as archivo:
                datos_matriz = archivo.read()
            # Convertir a matriz
            filas = datos_matriz.split("\n")
            longitud_fila_referencia = len(filas[0].split(" "))  # Longitud de la primera fila
            matriz_cargada = []
            for fila in filas:
                columna_str = fila.split(" ")
                columna_num = []
                # Verificar longitud de fila
                if len(columna_str) == longitud_fila_referencia:
                    for elemento in columna_str:
                        try:
                            elemento_num = int(elemento)
                        except ValueError:
                            pass
                        columna_num.append(elemento_num)
                # agregar fila solo si tiene la longitud correcta
                if columna_num:
                    matriz_cargada.append(columna_num)
            # actualizar la matriz del objeto
            self.matriz = matriz_cargada
            return True
        except:
            print('No existe el archivo')
            return False

    def editar_imagen(self, x, y, valorid): #Cambia un valor de la matriz
        self.matriz[x][y] = valorid

    def cargar_imagen(self):
        pantalla.fill((245,245,245))
        for fila in range(0, len( self.matriz )-1 ):     #Numero de cuadros en el eje x
            for columna in range( 0, len( self.matriz[0] )-1 ):     # Numero de cuadros en el eje y
                for elemento in colores:
                    try:
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
                    except:
                        pass
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
        self.matriz = convertir_columnas_a_filas(self.matriz)
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
        self.matriz = reflejo_matriz_ver(self.matriz)
        print(self.matriz)
        self.cargar_imagen()
    
    def actualizar_rects_nuevos(self):
        self.matriz_rects = actualizar_rects(self.matriz)

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
        self.tamaño_imagen = tamaño_imagen
        self.imagen = pygame.transform.scale(self.imagen,(tamaño_imagen,tamaño_imagen))
        self.posicion_x = posicion_x  
        self.posicion_y = posicion_y  
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

#Color parametros: nombre,id,tamanio,posicion x(se multiiplica por el tamanio del cuadro), posicion y
colores = [['amarillo',2,40,20,20 ],
           ['celeste',1,40,20,70],
           ['gris',8,40,20,120],
           ['morado',7,40,20,170],
           ['naranja',3,40,750,20],
           ['rojo',4,40,750,70],
           ['rosado',5,40,750,120],
           ['verde',6,40,750,170],
           ['blanco',0,40,750,220],
           ['negro',9,40,750,270]]

objetos_colores=[]
for fila in colores:#cargar los colroes en pantalla
    color = Color(f'colores/{fila[0]}.png',fila[1],fila[2],fila[3],fila[4],fila[0]) #Colores objetos
    objetos_colores.append(color)


# imagen,posicionx,posisicony,tamaño,funcion
iconos=[
    ["iconos/rotar_izq.png",20,220,40,"rotar_izq"],
    ["iconos/rotar_der.png",20,270,40,"rotar_der"],
    ['numeros/0.png',20,320,40,'matriz_num'],
    ['asciiart/9.png',20,370,40,'matriz_ascii'],
    ['iconos/contraste.png',20,420,40,'alto_contraste'],
    ['iconos/negativo.jpg',20,470,40,'negative'],
    ["iconos/borrador.png",20,520,40,"borrar"],
    ["iconos/ref_hor.png",20,570,40,"ref_hor"],
    ["iconos/ref_vert.png",20,620,40,"ref_vert"],
    ["iconos/zoomin.jpg",750,320,40,"zoom"],
    ["iconos/zoomout.png",750,370,40,"zoomout"],
    ["iconos/cerrar.png",750,420,40,"cerrar"],
    ["iconos/guardar.png",750,470,40,"guardar"]
]


iconos_objetos = []
for fila in iconos:
    icono = Iconos(fila[0],fila[1],fila[2],fila[3],fila[4])
    iconos_objetos.append(icono)
#iconos para el menu
menuiconos=[
    ["menu/nuevo.png",400,250,200,"crearnuevo"],
    ["menu/cargar.png",400,500,200,"cargar"]
]
fondomenu = pygame.image.load("menu/fondo_principal.jpg")
fondomenu = pygame.transform.scale( fondomenu , ( 1000 , 720 ) )
letras = pygame.image.load("menu/paintxel.png")
letras = pygame.transform.scale( letras , ( 600 , 100 ) )

menu_iconos=[]
for fila in menuiconos:
    menuicono = Iconos(fila[0],fila[1],fila[2],fila[3],fila[4])
    menu_iconos.append(menuicono)

while jugar:

    #Logica
    posicion_raton = pygame.mouse.get_pos()
    rect_raton.center = posicion_raton #colocar el Rectangulo para el raton encima del raton
    if menu:
        pantalla.blit(fondomenu,(0,0))
        pantalla.blit(letras,(200,100) )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugar = False    
            if event.type == pygame.MOUSEBUTTONDOWN: 

                for elemento in menu_iconos:    
                    if rect_raton.colliderect( elemento.rect_icono ):
                        if elemento.funcion == "crearnuevo":
                            nuevo_archivo=nombre()
                            lienzo = Editor("", "Default", nuevo_archivo,ascii_art)
                            lienzo.crear_archivos()
                            lienzo.guardar_archivo()
                            menu=False
                        elif elemento.funcion == "cargar":
                            cargar_archivo=nombre()
                            lienzo = Editor("", "Default",cargar_archivo,ascii_art)
                            encontro = lienzo.cargar_matriz()
                            if encontro:
                                menu=False

        for elemento in menu_iconos:
            elemento.mostrar_icono()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugar = False         
            if event.type == pygame.MOUSEBUTTONDOWN: 
                #Detecta colsion con algun cuadro de la matriz,luego guarda en la matriz el cuadro modificado con el respectivo id del color
                for numfila,fila in enumerate(lienzo.matriz_rects) :
                    for numcolumna,columna in enumerate(fila):
                        if rect_raton.colliderect(columna):
                            lienzo.editar_imagen(numcolumna,numfila,id_seleccionado)#modifica la matriz de 0 con el id correspodiente al color
                            #print(lienzo.matriz)#ver matriz
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
                        elif elemento.funcion == "zoom":
                            tamaño_cuadros+=1
                            lienzo.cargar_imagen()
                            lienzo.actualizar_rects_nuevos()
                            actualizar_imagenes()
                        elif elemento.funcion == "zoomout":
                            tamaño_cuadros-=1
                            lienzo.tamaño_cuadros=tamaño_cuadros
                            lienzo.cargar_imagen()
                            lienzo.actualizar_rects_nuevos()
                            actualizar_imagenes()
                        elif elemento.funcion == "cerrar":
                            menu=True
                            lienzo.estado_programa ='Finalizado'
                        elif elemento.funcion == "guardar":
                            lienzo.guardar_archivo()

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
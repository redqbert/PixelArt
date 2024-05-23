#Importar bibliotecas
import pygame

pygame.init()

#Sa

# Clases
class Editor():
    # Atributos
    matriz_imagen = 0 #Todavia falta crear la matriz
    creador = ""
    estado_programa = ""
    #Falta agregar metodos


# Area para funciones 


# Area variables
tamaño_cuadros = 32
comienzo_dibujar_cuadros = 32 * 3
rect_raton = pygame.Rect(0,0,10,10)
rect_raton.centerx = 400

rect1 = pygame.Rect(0,0,tamaño_cuadros,tamaño_cuadros)
color_rect1 = (220,220,220)

# pygame setup
pantalla = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()

# Variable para determinar cuando se cierra la ventana
jugar = True

while jugar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False

    # Refrescar la pantalla por cada frame para quitar el frame anterior
    pantalla.fill("white")

    # Logica
    posicion_raton = pygame.mouse.get_pos()
    rect_raton.center = posicion_raton #colocar el rect para el raton encima del raton


    #La idea es que se cargue solo una vez al inicio,luego cuando detecte el mouse,hara que se vuelva a cargar si fuese que se selecciono un color
    for i in range(26):
        for j in range(17):
            if i == 2 and j == 3:
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
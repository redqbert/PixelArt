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

def generador_matriz():
    matriz = []
    for y in range(17):
        matriz.append([])
        for x in range(26):
            matriz_subgrupo = matriz[y]
            matriz_subgrupo.append(0) #Este es el relleno de todos los elementos
    return matriz
print(generador_matriz())


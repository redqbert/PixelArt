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


import pygame
import json
from assets.imagenes import icono

class Configuracion:

    def cargar_configuracion(self):
        """
        Lee las configuraciones de ancho de pantalla, alto de pantalla y nombre de ventana desde el archivo
        'configuracion.json'. Si el archivo no existe, imprime un mensaje de error.
        """
        try:
            with open('configuracion.json', 'r') as archivo:
                datos = json.load(archivo)
                self.configuracion = datos.get('configuracion', {})
        except FileNotFoundError:
            print("No se encontro archivo configuracion")

        ancho_pantalla = self.configuracion.get('ancho_pantalla')
        alto_pantalla = self.configuracion.get('alto_pantalla')
        nombre_ventana = self.configuracion.get('nombre_ventana')

        pygame.mixer.init()
        self.PANTALLA = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption(nombre_ventana)
        pygame.display.set_icon(icono)
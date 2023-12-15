from modulos.utilidades import *
from assets.imagenes import item

class Item:
    def __init__(self, x, y, tamaño, tipo):
        self.animaciones = self.crear_animaciones()
        reescalar_imagenes(self.animaciones, tamaño[0], tamaño[1])
        self.rectangulo_principal = self.animaciones[tipo][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y

        self.pasos = 0
        self.animacion_actual = self.animaciones[tipo]            
        self.bandera_colision = False 
        
        self.puntos_recolectados = False
    
    def crear_animaciones(self):
        """
        Crea y devuelve un diccionario de animaciones para diferentes tipos de Items.
        Returns:
            dict: Diccionario con las animaciones de los diferentes tipos de Items.
        """
        
        diccionario = {}
        diccionario["Estrella"] = item
        return diccionario
    
    def actualizar(self, pantalla, jugador):
        """
        Si todavia no se recolecaron los puntos del item, actualiza la posición y la animación del Item 
        en la pantalla.

        Parameters:
            pantalla (pygame.Surface): Superficie de la pantalla del juego.
            jugador (Jugador): Objeto Jugador para verificar colisiones.
        """
        
        if self.puntos_recolectados == False:
            self.animar(pantalla)
            self.chequear_colisiones(jugador)
        
    def animar(self, pantalla):
        """
        Animación del Item en la pantalla.
        Parameters: pantalla (pygame.Surface): Superficie de la pantalla del juego.
        """
        
        largo = len(self.animacion_actual)
        if self.pasos >= largo:
            self.pasos = 0

        pantalla.blit(self.animacion_actual[self.pasos], self.rectangulo_principal)
        self.pasos += 1
    
    def chequear_colisiones(self, jugador):
        """
        Verifica si el Item colisiona con el Jugador y realiza las acciones correspondientes.

        Parameters: jugador (Jugador): Objeto Jugador
        """
        
        if self.rectangulo_principal.colliderect(jugador.rectangulo_secundario):
            jugador.puntos += 200
            self.puntos_recolectados = True
            play_sonido(r"assets\sonidos\muerte_enemigo.mp3", jugador)
                
                
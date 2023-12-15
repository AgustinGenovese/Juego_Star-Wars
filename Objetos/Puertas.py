from modulos.utilidades import *
from assets.imagenes import *
        
class Puertas:
    def __init__(self, x, y, tipo, tamaño):
        self.animaciones = self.crear_animaciones()
        reescalar_imagenes(self.animaciones, tamaño[0], tamaño[1])
        self.rectangulo_principal = self.animaciones[tipo][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y
        
        self.tipo = tipo
        self.sonido = True
        
        self.animacion_actual = self.animaciones[tipo][0]
        
    def crear_animaciones(self):
        #Crea y devuelve un diccionario de animaciones para diferentes tipos de Puertas.
        
        diccionario = {}
        diccionario["Puerta_n1"] = puerta_nivel_1
        diccionario["Puerta_n2"] = puerta_nivel_2
        return diccionario
     
    def actualizar(self, pantalla, personaje_principal):
        self.animar(pantalla, personaje_principal) 
        
    def animar(self, pantalla, jugador):
        """
        Realiza la animación de la puerta en la pantalla junto con su sonido.

        Parameters:
            pantalla (pygame.Surface): Superficie de la pantalla del juego.
            jugador (Jugador): Objeto Jugador para verificar colisiones.
        """
        
        if self.rectangulo_principal.colliderect(jugador.rectangulo_principal):
            self.animacion_actual = self.animaciones[self.tipo][1]
            pantalla.blit(self.animacion_actual, self.rectangulo_principal)
            if self.tipo == "Puerta_n1" and self.sonido:
                play_sonido(r"assets\sonidos\muerte_enemigo.mp3", jugador)
                self.sonido = False
            elif self.tipo == "Puerta_n2" and self.sonido:
                play_sonido(r"assets\sonidos\muerte_enemigo.mp3", jugador)
                self.sonido = False
        else:
            self.animacion_actual = self.animaciones[self.tipo][0]
            pantalla.blit(self.animacion_actual, self.rectangulo_principal)
            self.sonido = True

    def tiene_personaje(self, personaje_principal):
        """ 
        Verifica si el personaje está sobre la puerta.
        
        Parameters: personaje_principal (Personaje): Objeto Personaje para verificar la posición.
        Returns: bool: True si el personaje está sobre la puerta, False en caso contrario.
        """
        
        return self.rectangulo_principal.colliderect(personaje_principal.rectangulo_principal)
    
    
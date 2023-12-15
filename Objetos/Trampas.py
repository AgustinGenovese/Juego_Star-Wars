from modulos.utilidades import *
from assets.imagenes import trampa_cortadora

class Trampas:
    def __init__(self, x, y, tamaño, tipo):
        self.animaciones = self.crear_animaciones()
        reescalar_imagenes(self.animaciones, tamaño[0], tamaño[1])
        self.rectangulo_principal = self.animaciones[tipo][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y

        self.pasos = 0
        self.animacion_actual = self.animaciones[tipo]            
        self.bandera_colision = False 
        
    def crear_animaciones(self):
        """
        Crea y devuelve un diccionario de animaciones para diferentes tipos de Trampas.
        """
        
        diccionario = {}
        diccionario["Giratoria"] = trampa_cortadora
        return diccionario
    
    def actualizar(self, pantalla, jugador):
        self.animar(pantalla)
        self.chequear_colisiones(jugador)
        
    def animar(self, pantalla):
        """
        Realiza la animación de la trampa en la pantalla.
        """
        
        for imagen in self.animacion_actual:
            pantalla.blit(imagen, self.rectangulo_principal)
        
    def chequear_colisiones(self, jugador): 
        """
        Verifica colisiones con el jugador y realiza acciones correspondientes.
        """
        
        if self.rectangulo_principal.colliderect(jugador.rectangulo_secundario):
            play_sonido(r"assets\sonidos\trampa.mp3", jugador)
            jugador.desplazamiento_y = jugador.potencia_salto
            jugador.esta_saltando = True
            jugador.rectangulo_principal.y -= 20
            jugador.rectangulo_secundario.y -= 20
            jugador.vida -= 50
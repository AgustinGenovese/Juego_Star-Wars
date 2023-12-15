import pygame
from assets.imagenes import *
from modulos.utilidades import *

class Disparo:
    def __init__(self, x, y, direccion, imagen):
        self.superficie =  imagen
        self.superficie = pygame.transform.scale(self.superficie,(10,10))
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = x
        self.rectangulo.centery = y
        self.direccion = direccion
        self.colisiono = False
     
    def actualizar(self, pantalla, enemigos = None, enemigo_final = None, trampas = None, jugador = None): 
        """
        Actualiza la posición de los disparos en base a su direccion.
        Se chequea si alguno colisiono y en el caso que no hayan colisionado, se blitea la imagen.
        """
        
        if self.direccion == "Derecha":
            self.rectangulo.x += 10
        elif self.direccion == "Izquierda":
            self.rectangulo.x -= 10
         
        if self.colisiono == False:    
            self.chequeo_colision(enemigos, enemigo_final, trampas, jugador)
            pantalla.blit(self.superficie, self.rectangulo)
        
    def chequeo_colision(self, enemigos = None, enemigo_final = None, trampas = None, jugador = None):   
        """
        Realiza chequeos de colisión del disparo con los elementos del juego
        Los chequeos se realizaran solamente cuando le queda vida a los elementos.
        
        Parameters:
            enemigos (list): Lista de enemigos
            enemigo_final (objeto): Enemigo final
            trampas (list): Lista de trampas
            jugador (objeto): Jugador
        """
        
        if jugador != None:
            if self.rectangulo.colliderect(jugador.rectangulo_secundario):
                self.colisiono = True
                jugador.vida -= 50
                        
        if enemigos != None:
            for enemigo in enemigos:
                if self.rectangulo.colliderect(enemigo.rectangulo_principal) and enemigo.animacion_actual != enemigo.animaciones["vida"]:
                    self.colisiono = True
                    enemigo.vida -= 10
                    if enemigo.vida <= 0:
                        play_sonido(r"assets\sonidos\muerte_enemigo.mp3", jugador)
        
        if enemigo_final != None:
            if self.rectangulo.colliderect(enemigo_final.rectangulo_secundario) and enemigo_final.animacion_actual != enemigo_final.animacion["Explosion"]:
                self.colisiono = True
                enemigo_final.vida -= 10

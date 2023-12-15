from modulos.configuracion import *
from modulos.utilidades import *
from assets.imagenes import *
from Objetos.disparo import Disparo
import random

class Enemigo_Final:
    def __init__(self, x, y, direccion, pantalla):
        self.animacion = self.crear_animaciones()
        reescalar_imagenes(self.animacion, 420, 140)
        self.rectangulo_principal = self.animacion[direccion][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y
        self.pantalla = pantalla
        
        self.rectangulo_secundario = pygame.Rect(x + 15, y + 15 , 500, 100) 
        self.rectangulo_sup = pygame.Rect(x + 75, y + 20 , 270, 10) 
        self.rectangulo_inf = pygame.Rect(x + 130, y + 105 , 250, 10)
        self.rectangulo_izq = pygame.Rect(x + 20 , y, 20, 140)
        
        self.explosion = explosion
        self.pasos = 0
        
        self.bandera_explosion = False
          
        self.animacion_actual = self.animacion[direccion]

        self.velocidad = 4
        self.vida = 300
        self.esta_muerto = False
        
        self.tiempo_anterior = pygame.time.get_ticks()
        self.frecuencia_animacion = 100
        
        self.lista_proyectiles_enemigo = []
        
        
    def crear_animaciones(self):
        """
        Crea un diccionario con las animaciones del enemigo final.
        """
        
        diccionario = {}
        diccionario["Halcon_milenario"] = enemigo_final
        diccionario["Explosion"] = explosion
        return diccionario                                

    def actualizar(self, pantalla, jugador):   
        """
        Actualiza el estado del enemigo final en la pantalla.

        Parámetros:
        - pantalla (pygame.Surface): Superficie de la pantalla del juego.
        - jugador (Jugador): Objeto del jugador para detectar colisiones y actualizar puntos.
        """
        self.jugador = jugador
        tiempo_actual = pygame.time.get_ticks()
        
        if self.vida > 0:
            self.animar(pantalla, jugador)  
            self.actualizar_proyectiles(pantalla)
            self.lanzar_proyectil_trampa()
        elif self.vida <= 0 and self.esta_muerto == False:
            self.esta_muerto = True
            jugador.puntos += 300
            self.bandera_explosion = True
            self.animacion_actual = self.animacion["Explosion"]
            
        if self.bandera_explosion:
            play_sonido(r"assets\sonidos\explocion enemigo final.mp3", jugador, 2)          
            
            largo = len(self.animacion_actual)
            if tiempo_actual - self.tiempo_anterior > self.frecuencia_animacion:
                self.tiempo_anterior = tiempo_actual

                if self.pasos < largo:
                    pantalla.blit(self.animacion_actual[self.pasos], self.rectangulo_principal) 
                    self.pasos += 1
                else:
                    self.pasos = 0

            self.bandera_explosion = False
                
                
    def animar(self, pantalla, jugador):
        """
        Realiza la animación del enemigo final en la pantalla.

        Parámetros:
                    pantalla (pygame.Surface): Superficie de la pantalla del juego.
                    jugador (Jugador): Objeto del jugador para detectar colisiones.
        """
        
        if not self.bandera_explosion:
            self.rectangulo_principal.y += self.velocidad
            self.rectangulo_secundario.y += self.velocidad  
            self.rectangulo_sup.y += self.velocidad
            self.rectangulo_izq.y += self.velocidad
            self.rectangulo_inf.y += self.velocidad
            self.chequear_colisiones(jugador)
            
            if self.esta_muerto == False:
                if self.rectangulo_principal.y >= 500:
                    self.velocidad = -self.velocidad  
                elif self.rectangulo_principal.y <= 0:
                    self.velocidad = abs(self.velocidad)
                
                pantalla.blit(self.animacion_actual[0], self.rectangulo_principal)  
        
    def chequear_colisiones(self, jugador): 
        """
        Verifica y maneja las colisiones del enemigo final con el jugador.
        """
        
        if self.rectangulo_sup.colliderect(jugador.rectangulo_principal):
            jugador.rectangulo_principal.x -= 20
            jugador.rectangulo_secundario.x -= 20
            jugador.rectangulo_secundario.y -= 20
            jugador.rectangulo_principal.y -= 20
        
        if self.rectangulo_inf.colliderect(jugador.rectangulo_principal):
            self.velocidad = - self.velocidad
            jugador.vida -= 100
            play_sonido(r"assets\sonidos\trampa.mp3", jugador)
        
        if self.rectangulo_izq.colliderect(jugador.rectangulo_principal):
            jugador.rectangulo_principal.x -= 20
            jugador.rectangulo_secundario.x -= 20
                 
    def lanzar_proyectil_trampa(self):
        """
        Genera proyectiles (disparos) de trampa de forma aleatoria junto con su sonido.
        """
        
        numero_aleatorio = random.randint(0, 20)
        y = self.rectangulo_principal.centery
        x = self.rectangulo_principal.left
        direccion = "Izquierda"
        
        if numero_aleatorio == 5:
            self.lista_proyectiles_enemigo.append(Disparo(x, y, direccion, disparo_r2d2))
            if self.jugador.vida > 0:
                play_sonido(r"assets\sonidos\ataque enemigo final.mp3", self.jugador)
    
    def actualizar_proyectiles(self, pantalla):
        """
        Actualiza y gestiona los proyectiles lanzados por el enemigo final.
        
        Parámetros: pantalla (pygame.Surface): Superficie de la pantalla del juego.
        """
        
        i = 0
        while i < len(self.lista_proyectiles_enemigo):
            p = self.lista_proyectiles_enemigo[i]
            p.actualizar(pantalla, None, None, None, self.jugador)

            # Verificar colisión y eliminar proyectil si colisionó
            if p.rectangulo.centerx < 0 or p.rectangulo.centerx > pantalla.get_width() or p.colisiono:
                self.lista_proyectiles_enemigo.pop(i)
            else:
                i += 1
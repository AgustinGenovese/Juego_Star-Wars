from modulos.configuracion import *
from modulos.utilidades import *
from assets.imagenes import *

class Enemigo:
    def __init__(self, x, y, plataforma, direccion, nivel) -> None:
        self.animaciones = self.crear_animaciones()
        reescalar_imagenes(self.animaciones, 80, 70)
        self.rectangulo_principal = self.animaciones[direccion][0].get_rect()   
        self.rectangulo_principal.y = y
        self.rectangulo_principal.x = x
        self.plataforma_enemigo = plataforma
        
        self.rectangulo_secundario = pygame.Rect(x - 5, y , 10, 70)
        self.bandera_rectangulo_sec = False
        self.nivel = nivel
        
        self.velocidad = 3
        self.pasos = 0
        self.animacion_actual = self.animaciones[direccion]

        self.vida = 100
        self.esta_muerto = False
        self.vida_recolectada = False    
        
        self.tiempo_anterior = pygame.time.get_ticks()
        self.frecuencia_animacion = 100
        
        self.velocidad_y = 0
        
        if self.rectangulo_principal.y == 0:
            self.colisiono = False
        else:
            self.colisiono = True
        
        self.desplazamiento_y = 0
        self.gravedad = 0.5
        
                
    def actualizar(self, pantalla, jugador, plataformas):
        """
        Actualiza el estado del enemigo en la pantalla.

        Parámetros:
        - pantalla (pygame.Surface): Superficie de la pantalla del juego.
        - jugador (Jugador): Objeto del jugador para detectar colisiones.
        - plataformas (list): Lista de plataformas en la pantalla.
        """
        
        if self.colisiono == False:
            self.aplicar_gravedad(pantalla, plataformas)
        
        if self.vida > 0:
            self.animar(pantalla)
            self.avanzar()
            self.chequear_colisiones(jugador)
            
        elif self.vida_recolectada == False:
            self.animacion_actual = self.animaciones["vida"]
            self.animar(pantalla) 
        elif self.vida_recolectada == True:
            return

    def aplicar_gravedad(self, pantalla, plataformas):
        """
        Aplica la gravedad al enemigo y verifica las colisiones con las plataformas.
        Solamente de los enemigos que tengan su eje "y" en 0.

        Parámetros:
        - pantalla (pygame.Surface): Superficie de la pantalla del juego.
        - plataformas (list): Lista de plataformas libres en el nivel.
        """
        
        if self.vida > 0:
            self.animar(pantalla)
            self.desplazamiento_y += self.gravedad
            self.rectangulo_principal.y += self.desplazamiento_y
            self.rectangulo_secundario.y += self.desplazamiento_y
            plataformas_disponibles = plataformas[:-2].copy()
            
            for plataforma in plataformas_disponibles:
                if self.rectangulo_secundario.colliderect(plataforma.rect_superior): 
                    self.desplazamiento_y = 0
                    self.rectangulo_principal.bottom = plataforma.rect_superior.top
                    self.rectangulo_secundario.bottom = plataforma.rect_superior.top
                    self.colisiono = True
                    self.plataforma_enemigo = plataforma
        else:
            self.colisiono = True
    
    def crear_animaciones(self):
        # Crea un diccionario con las animaciones del enemigo.
        
        diccionario = {}
        diccionario["Izquierda_n1"] = enemigo_camina_izquierda_n1
        diccionario["Derecha_n1"] = enemigo_camina_derecha_n1
        diccionario["Izquierda_n2"] = enemigo_camina_izquierda_n2
        diccionario["Derecha_n2"] = enemigo_camina_derecha_n2
        diccionario["vida"] = vida
        return diccionario
    
    def avanzar(self):
        """
        Avanza la posición del enemigo en la plataforma. Se verifica la posición en la plataforma 
        y se actualiza la animación según la dirección y nivel del enemigo.
        """
        
        #Las variables left y right representan las coordenadas izquierda y derecha de la platafoma
        left = (self.plataforma_enemigo.diccionario_plataforma["rectangulo"].left)
        right = (self.plataforma_enemigo.diccionario_plataforma["rectangulo"].right)

        # Si la animación actual del enemigo es caminar hacia la izquierda (nivel 2 o nivel 1),
        # se mueve hacia la izquierda y ajusta la posición del rectángulo secundario
        if self.animacion_actual == self.animaciones["Izquierda_n2"] or self.animacion_actual == self.animaciones["Izquierda_n1"]:
            self.rectangulo_principal.x -= self.velocidad
            self.rectangulo_secundario.x -= self.velocidad
            if self.bandera_rectangulo_sec == False:
                self.rectangulo_secundario.x += 83
                self.bandera_rectangulo_sec = True
                
        # Si la animación actual del enemigo es caminar hacia la derecha (nivel 2 o nivel 1),
        # se mueve hacia la derecha y ajusta la posición del rectángulo secundario    
        elif self.animacion_actual == self.animaciones["Derecha_n2"] or self.animacion_actual == self.animaciones["Derecha_n1"]:
            self.rectangulo_principal.x += self.velocidad
            self.rectangulo_secundario.x += self.velocidad
            if self.bandera_rectangulo_sec:
                self.rectangulo_secundario.x -= 83
                self.bandera_rectangulo_sec = False      
        
        match self.nivel:
            # Verificar límites de la plataforma y actualizar animación según el nivel
            # Si el enemigo se encuentra a la izquierda de la plataforma, cambiar animación a caminar a la derecha
            # Si el enemigo se encuentra a la derecha de la plataforma, cambiar animación a caminar a la izquierda
            case 1:
                if self.rectangulo_principal.x < left - 20:
                    self.animacion_actual = self.animaciones["Derecha_n1"]
                if self.rectangulo_principal.x > right - 70:
                    self.animacion_actual = self.animaciones["Izquierda_n1"]
            case 2:
                if self.rectangulo_principal.x < left - 20:
                    self.animacion_actual = self.animaciones["Derecha_n2"]
                if self.rectangulo_principal.x > right - 70:
                    self.animacion_actual = self.animaciones["Izquierda_n2"]
    
    def animar(self, pantalla):
        # Realiza la animación automatica del enemigo en la pantalla.
        
        largo = len(self.animacion_actual)

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_anterior > self.frecuencia_animacion:
            self.tiempo_anterior = tiempo_actual

            self.pasos += 1
            if self.pasos >= largo:
                self.pasos = 0
            
        pantalla.blit(self.animacion_actual[self.pasos], self.rectangulo_principal)
    
    def chequear_colisiones(self, jugador):      
        """
        Verifica las colisiones del enemigo con el jugador y actualiza la animación en caso que el enemigo.
        En caso que colisiones, modificia la posicion del jugador, del enemigo y la vida.
        
        El match se utiliza para diferenciar los dos tipos de enemigos porque tienen animaciones distintas
        """
        
        if not self.esta_muerto:
            match self.nivel:
                case 1:
                    if self.animacion_actual == self.animaciones["Izquierda_n1"]:
                        if jugador.rectangulo_secundario.colliderect(self.rectangulo_principal):
                            jugador.rectangulo_principal.x -= jugador.velocidad + 1
                            jugador.rectangulo_secundario.x -= jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        elif jugador.rectangulo_principal.colliderect(self.rectangulo_secundario):    
                            self.animacion_actual = self.animaciones["Derecha_n1"]
                            jugador.rectangulo_principal.x -= jugador.velocidad + 1
                            jugador.rectangulo_secundario.x -= jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        else:
                            self.velocidad = 3
                            
                    if self.animacion_actual == self.animaciones["Derecha_n1"]:   
                        if jugador.rectangulo_secundario.colliderect(self.rectangulo_principal):
                            jugador.rectangulo_principal.x += jugador.velocidad + 1
                            jugador.rectangulo_secundario.x += jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        elif jugador.rectangulo_principal.colliderect(self.rectangulo_secundario):    
                            self.animacion_actual = self.animaciones["Izquierda_n1"]
                            jugador.rectangulo_principal.x += jugador.velocidad + 1
                            jugador.rectangulo_secundario.x += jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        else:
                            self.velocidad = 3
                            
                case 2:
                    if self.animacion_actual == self.animaciones["Izquierda_n2"]:
                        if jugador.rectangulo_secundario.colliderect(self.rectangulo_principal):
                            jugador.rectangulo_principal.x -= jugador.velocidad + 1
                            jugador.rectangulo_secundario.x -= jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        elif jugador.rectangulo_principal.colliderect(self.rectangulo_secundario):    
                            self.animacion_actual = self.animaciones["Derecha_n2"]
                            jugador.rectangulo_principal.x -= jugador.velocidad + 1
                            jugador.rectangulo_secundario.x -= jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        else:
                            self.velocidad = 3
                            
                    if self.animacion_actual == self.animaciones["Derecha_n2"]:   
                        if jugador.rectangulo_secundario.colliderect(self.rectangulo_principal):
                            jugador.rectangulo_principal.x += jugador.velocidad + 1
                            jugador.rectangulo_secundario.x += jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        elif jugador.rectangulo_principal.colliderect(self.rectangulo_secundario):    
                            self.animacion_actual = self.animaciones["Izquierda_n2"]
                            jugador.rectangulo_principal.x += jugador.velocidad + 1
                            jugador.rectangulo_secundario.x += jugador.velocidad + 1
                            self.velocidad = 0
                            jugador.vida -= 5
                            play_sonido(r"assets\sonidos\ataque enemigo.mp3", jugador)
                        else:
                            self.velocidad = 3              
                            
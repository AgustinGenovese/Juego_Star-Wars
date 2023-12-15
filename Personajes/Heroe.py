from modulos.configuracion import *
from modulos.utilidades import *
from assets.imagenes import *
from assets.sonidos import *
from Objetos.disparo import Disparo
from Personajes.Enemigo import Enemigo

class Heroe():
    def __init__(self, tamaño, pos_x, pos_y, velocidad) -> None:
        self.animaciones = self.crear_animaciones() 
        reescalar_imagenes(self.animaciones, tamaño[0], tamaño[1])
        self.rectangulo_principal = self.animaciones["Quieto_derecha"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.velocidad = velocidad
        
        self.rectangulo_secundario = pygame.Rect(pos_x + 5, pos_y + 30, 20, 70)
        
        self.que_hace = "Quieto"
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["Quieto_derecha"]

        self.desplazamiento_x = 0
        self.desplazamiento_y = 0
        self.potencia_salto = -13
        self.limite_velocidad_salto = 13
        self.gravedad = 1
        self.esta_saltando = False
        self.contador_saltos = 0
        
        self.vida = 500
        self.puntos = 0
        self.lista_proyectiles = []
        
        self.nivel_1_superado = False
        self.nivel_2_superado = False
        self.nivel_3_superado = False
        self.nivel_fin = True
        
        self.RELOJ = pygame.time.Clock()
        self.tiempo_inicial = pygame.time.get_ticks()
        
        self.sonido = True
        self.musica = True
        self.guardado = False
        self.cargado = False
                        
    def crear_animaciones(self):
        #Crea las animaciones del Heroe
        
        diccionario = {}
        diccionario["Quieto_derecha"] = personaje_quieto_derecha
        diccionario["Quieto_izquierda"] = personaje_quieto_izquierda
        diccionario["Derecha"] = personaje_camina_derecha
        diccionario["Izquierda"] = personaje_camina_izquierda
        return diccionario        
    
    def actualizar_personaje(self, pantalla, plataformas, enemigos = None, enemigo_final = None, trampas = None):  
        """
        La función actualiza la animación del personaje según su estado y dirección.
        
        - Gestiona la reproducción de sonidos, como los pasos del personaje.
        - Actualiza los proyectiles del personaje y su interacción con enemigos, el enemigo final y trampas.
        - Controla la posición del personaje en pantalla y lo "elimina" de pantallasi su vida llega a cero.
        
        Parameters:
        - pantalla (pygame.Surface): Superficie de la pantalla del juego.
        - plataformas (list): Lista de instancias de plataformas en el juego.
        - enemigos (list, optional): Lista de instancias de enemigos. Default: None.
        - enemigo_final (obj, optional): Instancia del enemigo final. Default: None.
        - trampas (list, optional): Lista de instancias de trampas. Default: None.
        """
                
        if self.vida > 0:
            global CONTADOR_DIRECCION
            match self.que_hace:
                case "Derecha":
                    if not self.esta_saltando:       
                        self.animacion_actual  = self.animaciones["Derecha"]
                        self.animar(pantalla)
                        CONTADOR_DIRECCION = 0
                        play_sonido(r"assets\sonidos\pasos.wav", self)
                    self.caminar(pantalla)
                
                case "Izquierda":
                    if not self.esta_saltando:
                        self.animacion_actual  = self.animaciones["Izquierda"]
                        self.animar(pantalla)
                        CONTADOR_DIRECCION = 1
                        play_sonido(r"assets\sonidos\pasos.wav", self)
                    self.caminar(pantalla)
                    
                case "Quieto":
                    if not self.esta_saltando:   
                        try:
                            match CONTADOR_DIRECCION:
                                case 0:
                                    self.animacion_actual = self.animaciones["Quieto_derecha"]  
                                case 1:
                                    self.animacion_actual = self.animaciones["Quieto_izquierda"]
                        except NameError:
                            CONTADOR_DIRECCION = 0
                            self.animacion_actual = self.animaciones["Quieto_derecha"]
                        self.animar(pantalla)
                                
                case "Salta":
                        self.esta_saltando = True
                        self.desplazamiento_y = self.potencia_salto   
                        self.animar(pantalla)
                                                
            self.actualizar_proyectiles(pantalla, enemigos, enemigo_final, trampas)
            self.aplicar_gravedad(pantalla, plataformas)
            self.verificar_limites(pantalla)
            self.recolectar_vida(enemigos)  
            self.modificar_rect_secundario() 
                        
        else:
            self.rectangulo_principal.x = 2000
            self.rectangulo_secundario.x = 2000
            return
            
    def caminar(self, pantalla):
        """
        Desplaza al personaje en la dirección especificada por su estado (Derecha o Izquierda).

        Observaciones:
        - Calcula la nueva posición en el eje x y verifica que esté dentro de los límites de la pantalla.
        - Actualiza las posiciones de los rectángulos principal y secundario del personaje.
        """
        
        velocidad_actual = self.velocidad
        if self.que_hace == "Izquierda":
            velocidad_actual *= -1    
        
        nueva_x = self.rectangulo_principal.x + velocidad_actual
        if nueva_x >= 0 and nueva_x <= pantalla.get_width() - self.rectangulo_principal.width:
            self.rectangulo_principal.x += velocidad_actual
            self.rectangulo_secundario.x += velocidad_actual
    
    def animar(self, pantalla):
        """
        Animación del personaje en la pantalla.

        Observaciones:
        - Calcula la longitud de la animación actual.
        - Restablece el contador de pasos si el personaje está saltando.
        - Blitea la imagen correspondiente según el contador de pasos en la posición del rectángulo principal.
        - Incrementa el contador de pasos para la siguiente animación.
        """
        
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        
        if self.esta_saltando == True: #si esta saltando solo blitea la imagen en posicion 0
            self.contador_pasos = 0
            
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1
                    
    def aplicar_gravedad(self, pantalla, plataformas):     
        
        if self.esta_saltando: 
            #realiza cambios en "y" progresivo
            self.animar(pantalla)
            self.rectangulo_principal.y += self.desplazamiento_y
            self.rectangulo_secundario.y += self.desplazamiento_y
            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad 
                
        if self.rectangulo_principal.y < 0:           
            #chequea limites pantalla superior
                self.rectangulo_principal.y = 0
                self.rectangulo_secundario.y = 0   

        piso = plataformas[0]
        piso_superior = piso.rect_superior   
        for plataforma in plataformas:
            if self.rectangulo_secundario.colliderect(plataforma.rect_inferior): 
                #Chequea que colpee la cabeza con la parte de abajo de la plataforma
                self.desplazamiento_y = 0
                self.esta_saltando = False
                if self.rectangulo_secundario.bottom != piso_superior.top:
                    #lo ubica el el piso
                    self.rectangulo_principal.y += 20
                    self.rectangulo_secundario.y += 20
                break
            
            elif self.rectangulo_secundario.colliderect(plataforma.rect_superior):
                #Chequea que golpee con el piso
                self.desplazamiento_y = 0
                self.esta_saltando = False
                self.rectangulo_principal.bottom = plataforma.rect_superior.top
                self.rectangulo_secundario.bottom = plataforma.rect_superior.top
                self.contador_saltos = 0
                break
            else:
                self.esta_saltando = True
                
    def lanzar_proyectil(self):
        """
        Lanza un proyectil en la dirección actual del personaje.

        Observaciones:
        - Reproduce el sonido de disparo.
        - Calcula la posición y dirección del proyectil según la animación actual del personaje.
        - Crea una instancia de la clase Disparo y la añade a la lista de proyectiles.
        """
    
        play_sonido(r"assets\sonidos\disparo.mp3", self)
        x = None
        margen = 47
        
        y = self.rectangulo_principal.centery - 9
        if self.animacion_actual == self.animaciones["Quieto_derecha"] or self.animacion_actual == self.animaciones["Derecha"]:
            x = self.rectangulo_principal.right + 40 - margen
            direccion = "Derecha"
        elif self.animacion_actual == self.animaciones["Quieto_izquierda"] or self.animacion_actual == self.animaciones["Derecha"]:
            x = self.rectangulo_principal.left - 50 + margen
            direccion = "Izquierda"
            
        if x is not None:
            self.lista_proyectiles.append(Disparo(x, y, direccion, disparo_simple))
        
    def actualizar_proyectiles(self, pantalla, enemigos=None, enemigo_final=None, trampas=None):
        """
        Actualiza y gestiona los proyectiles lanzados por el personaje.

        Observaciones:
        - Itera sobre la lista de proyectiles del personaje y actualiza cada uno.
        - Verifica las colisiones de los proyectiles con los enemigos, el enemigo final y las trampas.
        - Elimina los proyectiles que han colisionado o se han salido de la pantalla.
        """
        
        i = 0
        while i < len(self.lista_proyectiles):
            p = self.lista_proyectiles[i]
            p.actualizar(pantalla, enemigos, enemigo_final, trampas, self)

            # Verificar colisión y eliminar proyectil si colisionó
            if p.rectangulo.centerx < 0 or p.rectangulo.centerx > pantalla.get_width() or p.colisiono:
                self.lista_proyectiles.pop(i)
            else:
                i += 1
                
    def verificar_limites(self, pantalla):
        #Verifica y corrige si el personaje se encuentra fuera de los límites de la pantalla.
        
        if self.rectangulo_principal.x > pantalla.get_width():
            self.rectangulo_principal.x -= 1
            self.rectangulo_secundario.x -= 1

        if self.rectangulo_principal.x < 0:
            self.rectangulo_principal.x += 1
            self.rectangulo_secundario.x += 1
            
    def recolectar_vida(self, enemigos):
        """
        Recolecta vida al colisionar con enemigos.
        
        Observaciones:
        - Itera sobre la lista de enemigos para verificar si su vida ya fue recolectada.
        - Si la vida no ha sido recolectada y hay colisión con el personaje, aumenta la vida y puntaje del jugador.
        - Marca la vida del enemigo como recolectada y lo considera muerto.
        - Reproduce un sonido de recolección de vida.
        """
        
        for enemigo in enemigos:
            if enemigo.vida_recolectada == False:
                if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal) and enemigo.animacion_actual == enemigo.animaciones["vida"]:
                    self.vida += 50
                    self.puntos += 100
                    enemigo.vida_recolectada = True
                    enemigo.esta_muerto = True
                    play_sonido(r"assets\sonidos\vida.wav", self)

    def modificar_rect_secundario(self):
        if self.animacion_actual == self.animaciones["Quieto_izquierda"] or self.animacion_actual == self.animaciones["Izquierda"]:
            self.rectangulo_secundario.x = self.rectangulo_principal.x + 50
        elif self.animacion_actual == self.animaciones["Quieto_derecha"] or self.animacion_actual == self.animaciones["Derecha"]:
            self.rectangulo_secundario.x = self.rectangulo_principal.x

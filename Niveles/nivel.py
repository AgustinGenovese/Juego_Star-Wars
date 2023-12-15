import pygame
from Niveles.modo import *
from Objetos.disparo import Disparo
from assets.sonidos import *
from modulos.utilidades import *
import json
import os

class Nivel():
    def __init__(self, pantalla, lista_plataformas, lista_enemigos, lista_trampas, 
                 imagen_fondo, item, proximo_nivel = None, enemigo_final = None, puerta = None):
        
        self.pantalla = pantalla
        self.plataformas = lista_plataformas
        self.enemigos = lista_enemigos
        self.trampas = lista_trampas
        self.imagen_fondo = imagen_fondo
        self.puerta = puerta
        self.enemigo_final = enemigo_final
        self.item = item
        self.tiempo_ultimo_disparo = 0
        self.proximo_nivel = proximo_nivel
        self.gano = False
        self.FPS = 60
        self.RELOJ = pygame.time.Clock()
        self.tiempo_inicial = pygame.time.get_ticks()
        self.bandera_nivel_2 = True
                
    def actualizar_ciclo(self, lista_eventos, jugador):
        """
        Actualiza el ciclo principal del juego.
        Parameters:
            lista_eventos (list): Lista de eventos del juego.
            jugador (objeto): Instancia del objeto jugador
            
        Observaciones:
            - La función actualiza el reloj del juego y calcula el tiempo transcurrido.
            - Maneja eventos de teclado para cambiar el modo del juego y realizar saltos.
            - Realiza acciones adicionales según el tiempo transcurrido y el estado del jugador.
            - Guarda o carga la partida según la acción del jugador.
            - Actualiza el fondo y lee los inputs del usuario.
        """
        
        self.jugador = jugador
        self.RELOJ.tick(self.FPS)

        self.tiempo_actual = pygame.time.get_ticks()            
        tiempo_transcurrido = self.tiempo_actual - self.tiempo_inicial
            
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    cambiar_modo()
                elif event.key == pygame.K_SPACE:
                    play_sonido(r"assets\sonidos\jump.mp3", jugador)
                    if jugador.contador_saltos < 2:
                        jugador.contador_saltos += 1
                        jugador.que_hace = "Salta"  
        
        if (lambda tiempo: tiempo < 60000)(tiempo_transcurrido):
            if self.jugador.guardado:
                self.guardar_partida()
            if self.jugador.cargado:
                self.cargar_partida()
            self.actualizar_fondo(tiempo_transcurrido)
            self.leer_inputs(tiempo_transcurrido)
        else:
            self.bliteo_aviso_sin_tiempo()

    
    def actualizar_fondo(self, tiempo_transcurrido):
        """
        Renderiza los elementos en pantalla.
        
        Parameters:
            tiempo_transcurrido (int): El tiempo transcurrido desde el inicio del nivel.
        Observaciones:
            - Ajusta la posición del jugador al inicio del Nivel_tres si la bandera_nivel_2 está activa.
        """ 
        
        self.pantalla.blit(self.imagen_fondo, (0, 0))
    
        if self.plataformas != None:
            for plataforma in self.plataformas:
                if plataforma.esta_visible:
                    plataforma.diccionario_plataforma["superficie"]
                    self.pantalla.blit(plataforma.diccionario_plataforma["superficie"], 
                                    plataforma.diccionario_plataforma["rectangulo"])

        if self.puerta != None and self.enemigo_final == None:
            self.puerta.actualizar(self.pantalla, self.jugador)
         
        if self.trampas is not None:
            for trampa in self.trampas:
                trampa.actualizar(self.pantalla, self.jugador)
                
        if self.enemigo_final != None:
            if self.enemigo_final.esta_muerto:
                self.puerta.actualizar(self.pantalla, self.jugador)
            self.enemigo_final.actualizar(self.pantalla, self.jugador)            
        
        if self.item is not None:
            for item in self.item:
                item.actualizar(self.pantalla, self.jugador)
               
        if self.enemigos is not None:
            for enemigo in self.enemigos:
                enemigo.actualizar(self.pantalla, self.jugador, self.plataformas)
        
        if self.proximo_nivel == "Nivel_tres" and self.bandera_nivel_2:
            self.jugador.rectangulo_principal.y = 525
            self.jugador.rectangulo_secundario.y = 525
            self.bandera_nivel_2 = False

        self.jugador.actualizar_personaje(self.pantalla, self.plataformas, self.enemigos, self.enemigo_final, self.trampas)
        
        self.bliteo_informacion_personaje(tiempo_transcurrido)
        
    def leer_inputs(self, tiempo_transcurrido):
        """
        Lee las entradas de teclado y realiza acciones correspondientes al juego.
        Parameters:
            tiempo_transcurrido (int): El tiempo transcurrido desde el inicio del nivel.

        Observaciones:
            - Detecta las teclas presionadas para mover al personaje a la derecha, izquierda o dejarlo quieto.
            - Detecta la tecla 'A' para pasar al siguiente nivel si el personaje está en la puerta.
            - Lanza un proyectil si la tecla 'D' está presionada y ha pasado un tiempo suficiente desde el último disparo.
        """
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            self.jugador.que_hace = "Derecha"

        elif teclas[pygame.K_LEFT]:
            self.jugador.que_hace = "Izquierda"
    
        elif teclas[pygame.K_a]:
            if self.puerta.tiene_personaje(self.jugador):
                self.pasar_de_nivel()
                self.habilitar_nivel_superado(self.jugador)
                self.sumar_puntos(tiempo_transcurrido)    
        else:
            self.jugador.que_hace = "Quieto"
            
        if teclas[pygame.K_d]:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_disparo > 100:
                self.jugador.lanzar_proyectil()
                self.tiempo_ultimo_disparo = tiempo_actual
                        
        self.dibujar_rectangulos()
        
    def dibujar_rectangulos(self):
        """
        Dibuja rectángulos de colisión para elementos en el juego con el modo de depuración activado.

        Observaciones:
            - Dibuja rectángulos azules alrededor del personaje (jugador).
            - Dibuja rectángulos rojos alrededor de las plataformas, enemigos y enemigo final, si existen.
        """
        
        if obtener_modo():
            pygame.draw.rect(self.pantalla, "blue", self.jugador.rectangulo_principal, 3)
            pygame.draw.rect(self.pantalla, "blue", self.jugador.rectangulo_secundario, 3)
             
            if self.plataformas != None:
                for plataforma in self.plataformas:
                    pygame.draw.rect(self.pantalla, "red", plataforma.rect_superior, 1)
                    pygame.draw.rect(self.pantalla, "red", plataforma.rect_inferior, 1)
                    pygame.draw.rect(self.pantalla, "red", plataforma.rect_izquierdo, 1)
                    pygame.draw.rect(self.pantalla, "red", plataforma.rect_derecho, 1)
            
            if self.enemigos != None:
                for enemigo in self.enemigos:
                    pygame.draw.rect(self.pantalla, "red", enemigo.rectangulo_secundario, 3)    
                    pygame.draw.rect(self.pantalla, "red", enemigo.rectangulo_principal, 3)
            
            if self.enemigo_final != None:
                pygame.draw.rect(self.pantalla, "red", self.enemigo_final.rectangulo_principal, 3)    

    def pasar_de_nivel(self):
        self.gano = True
        
    def sumar_puntos(self, tiempo_transcurrido) :
        #Calcula puntos por tiempo
        self.jugador.puntos += int((tiempo_transcurrido * 0.001) * 100)

    def bliteo_aviso_sin_tiempo(self):
        #Blitea pantalla de perdida
        if self.jugador.vida > 0 and self.jugador.nivel_3_superado == False :
            self.pantalla.fill("black")
            fuente = pygame.font.SysFont("Verdana", 50)
            aviso = fuente.render(f"Se te acabo el tiempo", False, "white")
            self.pantalla.blit(aviso, (265, 130))   
    
    def bliteo_informacion_personaje(self, tiempo_transcurrido):
        fuente = pygame.font.SysFont("Verdana", 20)
        texto_puntos_vida = fuente.render(f"Vida: {self.jugador.vida} Puntos: {self.jugador.puntos}", False, "white")
        self.pantalla.blit(texto_puntos_vida, (30, 30)) 
            
        if self.proximo_nivel == None:
            fuente = pygame.font.SysFont("Verdana", 50)
            aviso_ganador = fuente.render(f"Ganador!", True, "white")
            self.pantalla.blit(aviso_ganador, (370, 130))  
                  
        else:
            fuente = pygame.font.SysFont("Verdana", 20)
            tiempo_segundos = int(tiempo_transcurrido * 0.001)
            texto_tiempo = fuente.render(f"Segundos: {tiempo_segundos}", False, "white")
            self.pantalla.blit(texto_tiempo, (800, 30))  
        
        if self.jugador.vida <= 0:
            self.pantalla.fill("black")
            fuente = pygame.font.SysFont("Verdana", 50)
            aviso = fuente.render(f"GAME OVER", False, "white")
            self.pantalla.blit(aviso, (330, 130))
             
    def habilitar_nivel_superado(self, jugador):
        """
        Habilita el estado correspondiente al nivel superado en el objeto jugador.
        Parameters: jugador (objeto): Instancia del objeto jugador.
        """
        
        match self.proximo_nivel:
            case "Nivel_dos":
                jugador.nivel_1_superado = True
            case "Nivel_tres":
                jugador.nivel_2_superado = True
            case "Nivel_fin":
                jugador.nivel_3_superado = True
                jugador.nivel_fin = True
                
    def guardar_partida(self):
        """
        Guarda el estado actual de la partida en un archivo JSON.

        Observaciones:
            - Borra la partida anterior antes de guardar la nueva.
            - Restablece la bandera de guardado del jugador a False después de guardar la partida.
        """
        
        self.borrar_partida_anterior()    
        datos_partida = {
            'partida': {
                'jugador': self.to_dict("jugador"),
                'enemigo': self.to_dict("enemigo"),
                'enemigo_final': self.to_dict("enemigo_final"),
                'item': self.to_dict("item"),
                'proximo_nivel': self.proximo_nivel,       
                }
        }
        try:
            with open('partida.json', 'w') as archivo:
                json.dump(datos_partida, archivo, indent=4)
            print("partida guardada exitosamente.")
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
        
        self.jugador.guardado = False
    
    def borrar_partida_anterior(self):
        # Intenta borrar el archivo de la partida anterior si existe, no hace nada si el archivo no existe
        try:
            os.remove('partida.json')
            print("Partida anterior eliminada.")
        except FileNotFoundError:
            pass  
    
    def to_dict(self, param):     
        """
        Convierte los elementos necesarios para guardar la partida en un formato diccionario
        
        Parameters: param (str): Indica el atributo a guardar
        Returns: dict or list: Un diccionario o lista que contiene los atributos a guardar.
        """
        
        match param:
            case "jugador":
                return {
                    'x': self.jugador.rectangulo_principal.x,
                    'y': self.jugador.rectangulo_principal.y,
                    'x_sec': self.jugador.rectangulo_secundario.x,
                    'y_sec': self.jugador.rectangulo_secundario.y,
                    'vida': self.jugador.vida,
                    'punto': self.jugador.puntos
                }
            case "enemigo":
                lista_enemigos = []
                for i in range(len(self.enemigos)):
                    lista_enemigos.append(self.enemigos[i].vida)
                return lista_enemigos
             
            case "enemigo_final":
                if self.enemigo_final != None:
                    return {
                        'vida': self.enemigo_final.vida,
                    }
            case "item":
                lista_items = []
                if self.item != None:
                    for i in range(len(self.item)):
                        lista_items.append(self.item[i].puntos_recolectados)
                return lista_items
                        
    def cargar_partida(self):
        """
        Obtiene la informacion de larchivo Json por medio del metodo "cargar_partida_datos.
        Actualiza los atributos actuales, con los atributos guardados previamente
        """
        
        datos_partida = self.cargar_partida_datos()
        
        jugador_data = datos_partida.get('jugador', {})
        self.jugador.rectangulo_principal.x = jugador_data.get('x')
        self.jugador.rectangulo_principal.y = jugador_data.get('y')
        self.jugador.rectangulo_secundario.x = jugador_data.get('x_sec')
        self.jugador.rectangulo_secundario.y = jugador_data.get('y_sec')
        self.jugador.vida = jugador_data.get('vida')
        self.jugador.puntos = jugador_data.get('punto')
        self.bandera_nivel_2 = False

        enemigos_data = datos_partida['enemigo']
        for i in range(len(enemigos_data)):
            self.enemigos[i].vida = enemigos_data[i]
            if self.enemigos[i].vida <= 0:
                self.enemigos[i].vida_recolectada = True

        enemigo_final_data = datos_partida.get('enemigo_final', {})
        if self.enemigo_final:
            self.enemigo_final.vida = enemigo_final_data.get('vida')
            self.enemigo_final.sonido = False

        items_data = datos_partida['item']
        for i in range(len(items_data)):
            self.item[i].puntos_recolectados = items_data[i]
        
        self.jugador.cargado = False
    
    def cargar_partida_datos(self):
        """
        Obtiene la informacion de larchivo Json y la guarda en la variable datos_partida.
        """
        try:
            with open('partida.json', 'r') as archivo:
                datos_partida = json.load(archivo)
                return datos_partida.get('partida', {})
        except FileNotFoundError:
            print("No se encontró el archivo de partida.")
            return {}
        
        

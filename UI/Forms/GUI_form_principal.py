from assets.imagenes import fondo_inicio
import sqlite3
from UI.GUI_slider import *
from UI.Forms.GUI_form_menu_score import *
from UI.Forms.GUI_form_menu_play import *
from UI.GUI_textbox import TextBox
import json
    
class FormPrincipal(Form):
    def __init__(self, screen, x,y,w,h,color_background, color_border = "Black", border_size = -1, active = True):
        super().__init__(screen, x,y,w,h,color_background, color_border, border_size, active)

        self.manejador_niveles = Manejador_niveles(self._master)
        self._slave = pygame.Surface((w,h))
        self.ancho = w
        self.altura = h
        
        self.flag_player = True
        self.volumen = 0.2 
        
        pygame.mixer.init()
        pygame.mixer.music.load(r"UI\Recursos\menu_prin.mp3")
        pygame.mixer.music.play(-1)
        
        self.btn_jugar = Button(self._slave, x , y,
                            70,450,100,50, 
                            "white", "black", 
                            self.entrar_nivel,
                            "Nivel_uno", "Jugar", "Verdana", 15, "black")   
        
        self.btn_niveles = Button(self._slave, x , y,
                            300,450,100,50, 
                            "white", "black", 
                            self.btn_niveles_click,
                            "hola", "Niveles", "Verdana", 15, "black")
        
        self.btn_cargar = Button(self._slave, x , y,
                            550,450,110,50,  
                            "white", "black", 
                            self.btn_cargar_click,
                            "hola", "Cargar Partida", "Verdana", 15, "black")
        
        self.btn_puntajes = Button(self._slave, x , y,
                            810,450,100,50,  
                            "white", "black", 
                            self.btn_tabla_click,
                            "hola", "Puntajes", "Verdana", 15, "black")
        
        self.btn_play = Button(self._slave, x , y,
                            810,550,100,50, 
                            "white", "black", 
                            self.btn_play_click,
                            "hola", "Mute", "Verdana", 15, "black")

        self.slider_volumen = Slider(self._slave, x,y, 
                                    70,570,500,15, 
                                    self.volumen, 
                                    "white", "black")

        porcentaje_volumen= f"{self.volumen * 100}%" 
        self.btn_volumen = Button(self._slave, x , y,
                            650, 550, 100,50, 
                            "white", "black", 
                            self.btn_play_click,
                            "hola", porcentaje_volumen, "Verdana", 15, "black")
        
        self.lista_widgets.append(self.btn_play)
        self.lista_widgets.append(self.btn_volumen)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_puntajes )
        self.lista_widgets.append(self.btn_niveles)
        self.lista_widgets.append(self.btn_jugar)
        self.lista_widgets.append(self.btn_cargar)
    
    def render(self):
        fondo_inicial = pygame.transform.scale(fondo_inicio, (self.ancho,self.altura))
        self._slave.blit(fondo_inicial, (0,0))
        
        fuente = pygame.font.SysFont("rockwell", 70)
        titulo = fuente.render(f"Star Wars", True, "Black")
        self._slave.blit(titulo, (350, 40))
        fuente = pygame.font.SysFont("rockwell", 60)
        subtitulo = fuente.render(f"Revenge of the Stormtrooper", True, "Black")
        self._slave.blit(subtitulo, (100, 110))

    def update(self, lista_eventos, jugador):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)#POLIMORFISMO (CADA WIDGET SE ACTUALIZA DE MANERA DIFERENTE)
                self.update_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)
            
        self.jugador = jugador

    def update_volumen(self, lista_eventos):
        self.volumen = self.slider_volumen.value
        self.btn_volumen.update(lista_eventos)
        self.btn_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)
        
    def btn_play_click(self, param):
        if self.flag_player:
            pygame.mixer.music.pause()
            self.btn_play._color_background = "white"
            self.btn_play.set_text("Play") 
        else:
            pygame.mixer.music.unpause()
            self.btn_play._color_background = "white"
            self.btn_play.set_text("Mute") 
        
        self.flag_player = not self.flag_player
    
    def btn_tabla_click(self, param):
        with sqlite3.connect("base_datos_puntajes.db") as conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT Nombre, Puntaje FROM Jugadores ORDER BY Puntaje DESC LIMIT 3")
                filas = cursor.fetchall()

                diccionario_top3 = []
                for fila in filas:
                    diccionario = {"Jugador": fila[0], "Score": fila[1]}
                    diccionario_top3.append(diccionario)

            except Exception as e:
                print("Error:", e)
        
        nuevo_form = FormMenuScore(screen = self._master,
                                x = self._master.get_width() / 2 - 280,
                                y = self._master.get_height() / 2 - 120,
                                w = 550,
                                h = 300,
                                color_background = "green",
                                color_border = "black",
                                active = True,
                                scoreboard = diccionario_top3,
                                margen_x = 10,
                                margen_y = 100 ,
                                espacio = 10
                                   )
        
        self.show_dialog(nuevo_form)
        
    def btn_niveles_click(self, param):
        frm_jugar = FormMenuPlay(screen=self._master,
                                x = self._master.get_width() / 2 - 280,
                                y = self._master.get_height() / 2 - 120,
                                w = 550,
                                h = 225,
                                color_background = "white",
                                color_border = "black",
                                active = True, 
                                personaje = self.jugador,
                                menu = self
                                )
        
        self.show_dialog(frm_jugar)
               
    def entrar_nivel(self, nombre_nivel):
        nivel = self.manejador_niveles.get_nivel(nombre_nivel)
        frm_contenedor_nivel = FormContenedorNivel(self._master, nivel, nivel.proximo_nivel, self.manejador_niveles, self.jugador)
        self.show_dialog(frm_contenedor_nivel)
        
    def btn_cargar_click(self, param):
        self.jugador.cargado = True
        proximo_nivel = self.btn_cargar_proximo_nivel()
        
        match proximo_nivel:
            case "Nivel_dos":
                nivel = "Nivel_uno"
            case "Nivel_tres":
                nivel = "Nivel_dos"
            case "Nivel_fin":
                nivel = "Nivel_tres"
            case _:
                nivel = "Nivel_fin"
        
        self.entrar_nivel(nivel)
        
    def btn_cargar_proximo_nivel(self):
        with open('partida.json', 'r') as archivo:
            try:
                datos_partida = json.load(archivo)
                return datos_partida.get('partida', {}).get('proximo_nivel')
            except FileNotFoundError:
                print("No se encontró el archivo de partida.")
                return None
            
            
    
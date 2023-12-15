import sqlite3
import pygame
from pygame.locals import *
from UI.GUI_form import *
from UI.GUI_button_image import *
from UI.Forms.GUI_form_menu_pausa import MenuPausa 
from UI.GUI_textbox import *

class FormContenedorNivel(Form):
    def __init__(self, screen: pygame.Surface, nivel, proximo_nivel_str, manejador_niveles, jugador, menu = None):
        super().__init__(screen, 0, 0, screen.get_width(), screen.get_height(), "green")
        nivel._slave = self._slave
        self.nivel = nivel
        self.manejador_niveles = manejador_niveles
        self.proximo_nivel_str = proximo_nivel_str
        self.screen = screen
        self.jugador = jugador
        
        if self.jugador.musica:
            if self.proximo_nivel_str == "Nivel_dos":
                pygame.mixer.music.load(r"UI\Recursos\nivel_1.wav")
                pygame.mixer.music.play(-1)
            elif self.proximo_nivel_str == "Nivel_tres":
                pygame.mixer.music.load(r"UI\Recursos\nivel_2.mp3")
                pygame.mixer.music.play(-1)
            elif self.proximo_nivel_str == "Nivel_fin":
                pygame.mixer.music.load(r"UI\Recursos\nivel_3.wav")
                pygame.mixer.music.play(-1)
            elif self.proximo_nivel_str == None:
                pygame.mixer.music.load(r"UI\Recursos\nivel_fin.wav")
                pygame.mixer.music.play(-1)
        
        self.menu = menu

        self._btn_pausa = Button_Image(screen = self.screen,
                                       master_x = 0,
                                       master_y = 0,
                                       x = 50,
                                       y =  540,
                                       w= 50,
                                       h = 50,
                                       path_image = r"UI\Recursos\pausa.png",
                                       onclick = self.btn_pausa,
                                       onclick_param= ""
                                       )
        
        self._btn_puntaje = Button_Image(screen = self.screen,
                                       master_x = 0,
                                       master_y = 0,
                                       x = 370,
                                       y =  255,
                                       w= 240,
                                       h = 50,
                                       path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                       onclick = self.on,
                                       onclick_param= "",
                                       text = "Añadir puntaje",
                                       font = "Verdana",
                                       font_size = 14,
                                       font_color = "White",
                                       )
        
        self.txt_nombre = TextBox(self.screen, 0,0, 
                                440,305,170,50,
                                "gray", "white", "red", "blue", 2, 
                                "Comic Sans Ms", 15,"black")
        
        self.btn_nombre = Button_Image(screen = screen,
                                                master_x = 0,
                                                master_y = 0, 
                                                x = 370,
                                                y =  305,
                                                w = 80,
                                                h = 50,
                                                path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                                onclick = self.on,
                                                onclick_param= "",
                                                text= " Nombre:",
                                                font= "Verdana",
                                                font_size=  15,
                                                font_color="White"
                                                )   
                
        self.aceptar = Button_Image(screen = screen,
                                        master_x = 0,
                                        master_y = 0, 
                                        x = 370,
                                        y =  355,
                                        w = 240,
                                        h = 50,
                                        path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                        onclick = self.guardar_nombre,
                                        onclick_param= "",
                                        text= "Aceptar",
                                        font= "Verdana",
                                        font_size=  15,
                                        font_color="White"
                                        )   
        
        self.lista_widgets.append(self._btn_pausa)
        if jugador.nivel_3_superado and jugador.nivel_fin:
            self.lista_widgets.append(self._btn_puntaje)
            self.lista_widgets.append(self.txt_nombre)
            self.lista_widgets.append(self.btn_nombre)
            self.lista_widgets.append(self.aceptar)
                            
    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            self.nivel.actualizar_ciclo(lista_eventos, self.jugador)
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
                widget.draw()
            if self.nivel.gano:
                self.pasar_de_nivel()  
        else:
            self.hijo.update(lista_eventos)
        
    def btn_pausa(self, param):
        form_pausa = MenuPausa(screen = self._master,
                                x = 300,
                                y = 150,
                                w = 1,
                                h = 1,
                                color_background = "white",
                                color_border = "white",
                                active = True,
                                margen_x = 10,
                                margen_y = 100,
                                espacio = 10,
                                contenedor = self,
                                menu = self.menu,
                                jugador = self.jugador
                                )
        
        self.show_dialog(form_pausa)
    
    def pasar_de_nivel(self):
        self.padre.entrar_nivel(self.proximo_nivel_str)
        self.close()

    def on(self, parametro ):
        print("hola", parametro)
        
    def guardar_nombre(self, parametro):
        with sqlite3.connect("base_datos_puntajes.db") as conexion:
            try:
                nombre = self.txt_nombre.get_text()
                puntaje = self.jugador.puntos
                conexion.execute("INSERT INTO Jugadores(Nombre, Puntaje) VALUES (?, ?)", (nombre, puntaje))
                print("Dato insertado con éxito")
            except Exception as e:
                print("Error inserting data:", e)
                
        self.lista_widgets = self.lista_widgets[:-4]
        self.jugador.nivel_fin = False
import pygame
from pygame.locals import *
from UI.GUI_button_image import *
from UI.GUI_form import *
from Niveles.manejador_niveles import Manejador_niveles
from UI.Forms.GUI_form_contenedor_nivel import FormContenedorNivel
    
class FormMenuPlay(Form):
    def __init__(self, screen, x,y,w,h,color_background, color_border, active, personaje, menu):
        super().__init__(screen, x,y,w,h,color_background, color_border, active)

        self.manejador_niveles = Manejador_niveles(self._master)
        
        self._slave = pygame.Surface((w,h))
        self.ancho = w
        self.altura = h
        
        self.jugador = personaje
        
        self.menu = self
        
        self._slave.fill("white")
        pygame.draw.rect(self._slave, "black", (0,0,self.ancho,self.altura), 5)

        self._btn_level_1 = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = 45 ,
                                       y =  35,
                                       w = 140,
                                       h = 140,
                                       path_image = r"UI\Recursos\1.png",
                                       onclick = self.entrar_nivel,
                                       onclick_param= "Nivel_uno"
                                       ) 
        
        self._btn_level_2 = Button_Image(screen = self._slave,
                                    master_x = x,
                                    master_y = y, 
                                    x = 205 ,
                                    y = 35,
                                    w = 140,
                                    h = 140,
                                    path_image = r"UI\Recursos\2.png",
                                    onclick = self.entrar_nivel,
                                    onclick_param= "Nivel_dos"
                                        )
        
        self._btn_level_2_no_disp = Button_Image(screen = self._slave,
                                    master_x = x,
                                    master_y = y, 
                                    x = 205 ,
                                    y = 35,
                                    w = 140,
                                    h = 140,
                                    path_image = r"UI\Recursos\2_no_dispo.png",
                                    onclick = self.on,
                                    onclick_param= "Nivel_dos"
                                        )
                                       
        self._btn_level_3 = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = 365 ,
                                       y = 35,
                                       w = 140,
                                       h = 140,
                                       path_image = r"UI\Recursos\3.png",
                                       onclick = self.entrar_nivel,
                                       onclick_param= "Nivel_tres"
                                        )
        
        self._btn_level_3_no_disp = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = 365 ,
                                       y = 35,
                                       w = 140,
                                       h = 140,
                                       path_image = r"UI\Recursos\3_no_dispo.png",
                                       onclick = self.on,
                                       onclick_param= "Nivel_tres"
                                        )

        self.boton_home = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = 495,
                                       y =  170,
                                       w= 40,
                                       h = 40,
                                       path_image = r"UI\Recursos\home.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""
                                       )
        
        self.lista_widgets.append(self._btn_level_1)
        
        if self.jugador.nivel_2_superado:   
            self.lista_widgets.append(self._btn_level_2)
        else:
            self.lista_widgets.append(self._btn_level_2_no_disp)
        
        if self.jugador.nivel_3_superado:   
            self.lista_widgets.append(self._btn_level_3)
        else:
            self.lista_widgets.append(self._btn_level_3_no_disp)
        
        self.lista_widgets.append(self.boton_home)

    def on(self, parametro):
        print("", parametro)

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
        else:
            self.hijo.update(lista_eventos)
            
    def entrar_nivel(self, nombre_nivel):
        nivel = self.manejador_niveles.get_nivel(nombre_nivel)
        frm_contenedor_nivel = FormContenedorNivel(self._master, nivel, nivel.proximo_nivel, self.manejador_niveles, self.jugador, self.menu)
        self.show_dialog(frm_contenedor_nivel)

    def btn_home_click(self, param):
        self.end_dialog()
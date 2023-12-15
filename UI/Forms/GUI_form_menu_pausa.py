from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_slider import *
from UI.GUI_label import *
from UI.Forms.GUI_form_menu_score import FormMenuScore

class MenuPausa(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, margen_y, margen_x, espacio, contenedor, menu = None, jugador = None):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)
        self._slave = pygame.Surface((w,h))
        self.ancho = w
        self.altura = h      

        self.flag_player = True

        self.lista_eventos = None
        
        pygame.draw.rect(self._slave, "black", (0,0,self.ancho,self.altura), 5)
        
        self.lista_widgets = []      
        
        self.screen = screen
        
        self.contenedor = contenedor   
        self.menu = menu
        self.jugador = jugador
            
        self.btn_return = Button_Image(screen = screen,
                                        master_x = 0,
                                        master_y = 0, 
                                        x = 360,
                                        y =  200,
                                        w = 250,
                                        h = 50,
                                        path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                        onclick = self.btn_return,
                                        onclick_param= "",
                                        text= "Reanudar juego",
                                        font= "Verdana",
                                        font_size=  15,
                                        font_color="White"
                                        )    
        
        self.guardar = Button_Image(screen = screen,
                                        master_x = 0,
                                        master_y = 0, 
                                        x = 360,
                                        y =  250,
                                        w = 250,
                                        h = 50,
                                        path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                        onclick = self.guardar_partida_click,
                                        onclick_param= "",
                                        text= "Guardar partida",
                                        font= "Verdana",
                                        font_size=  15,
                                        font_color="White"
                                        )     
               
        self.mute = Button_Image(screen = screen,
                                        master_x = 0,
                                        master_y = 0, 
                                        x = 360,
                                        y =  300,
                                        w = 250,
                                        h = 50,
                                        path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                        onclick = self.btn_play_click,
                                        onclick_param= "",
                                        text= "Musica: Mute / Play",
                                        font= "Verdana",
                                        font_size=  15,
                                        font_color="White"
                                        )   
        
        self.mute_sonidos = Button_Image(screen = screen,
                                        master_x = 0,
                                        master_y = 0, 
                                        x = 360,
                                        y =  350,
                                        w = 250,
                                        h = 50,
                                        path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                        onclick = self.btn_mute_sonidos,
                                        onclick_param= "",
                                        text= "Sonidos: Mute / Play",
                                        font= "Verdana",
                                        font_size=  15,
                                        font_color="White"
                                        )   
        
        self.btn_menu_principal = Button_Image(screen = screen,
                                        master_x = 0,
                                        master_y = 0, 
                                        x = 360,
                                        y =  400,
                                        w = 250,
                                        h = 50,
                                        path_image = r"UI\Recursos\rectangulo_negro.PNG",
                                        onclick = self.btn_menu_principal_click,
                                        onclick_param= "",
                                        text= "Menu Principal",
                                        font= "Verdana",
                                        font_size=  15,
                                        font_color="White"
                                        )
         
        self.lista_widgets.append(self.btn_return)
        self.lista_widgets.append(self.mute)
        self.lista_widgets.append(self.mute_sonidos)
        self.lista_widgets.append(self.guardar)
        self.lista_widgets.append(self.btn_menu_principal)

    def on(self, parametro):
        print("hola", parametro)
    
    def update(self, lista_eventos):   
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
            
    def btn_return(self,parametro):
        self.end_dialog()
        
    def btn_play_click(self, param):
        if self.flag_player:
            pygame.mixer.music.pause()
            self.jugador.musica = False
        else:
            pygame.mixer.music.unpause()
            self.jugador.musica = True
        
        self.flag_player = not self.flag_player
    
    def btn_menu_principal_click(self, param):
        pygame.mixer.music.load(r"UI\Recursos\menu_prin.mp3")
        pygame.mixer.music.play(-1)
        
        self.jugador.vida = 500
        self.jugador.puntos = 0
        self.jugador.rectangulo_principal.x = 30
        self.jugador.rectangulo_secundario.x = 30
        self.jugador.rectangulo_principal.y = 60
        self.jugador.rectangulo_secundario.y = 60

        if self.menu != None:
            self.menu.end_dialog()
        
        self.contenedor.end_dialog()
        self.close()
    
    def btn_mute_sonidos(self, param):
        if self.jugador.sonido:
            self.jugador.sonido = False
        else:
            self.jugador.sonido = True
            
    def guardar_partida_click(self, param):
        self.jugador.guardado = True

import pygame
from pygame.locals import *

from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *

        
class FormMenuScore(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, scoreboard, margen_y,margen_x, espacio):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)
        
        self._slave = pygame.Surface((w,h))
        self.ancho = w
        self.altura = h
        
        self._slave.fill("white")
        pygame.draw.rect(self._slave, "black", (0,0,self.ancho,self.altura), 5)
        
        self._score = scoreboard
        self.lista_widgets = []

        self._margen_y = margen_y
        #Creo 2 labels y los agrego a la lista de widgets
        self.lista_widgets.append(
            Label(screen=self._slave, x=margen_x,y=20,w=w/2-margen_x-15,h=50,text = "Jugador", font="Verdana",font_size=30,font_color="white",path_image= r"UI\Recursos\rectangulo_negro.PNG"))
        self.lista_widgets.append(
            Label(screen=self._slave,
                x=margen_x+10+w/2-margen_x-10,
                y=20,w=w/2-margen_x-15,
                h=50,text = "Puntaje",
                font="Verdana",
                font_size=30,
                font_color="white",
                path_image= r"UI\Recursos\rectangulo_negro.PNG")
            )
        
        pos_inicial_y = margen_y
        
        #Encapsular esta logica en un metodo. Esto nos permite dibujar la tabla en pantalla
        
        for j in self._score:
            pos_inicial_x = margen_x
            for n,s in j.items():
                cadena = "" 
                cadena = f"{s}"
                pos = Label(screen=self._slave, x=pos_inicial_x,y=pos_inicial_y -15,
                            w=w/2-margen_x-10,h=50,text = cadena, font="Verdana",font_size=30,
                            font_color="black",path_image= r"UI\Recursos\Table.png")
                self.lista_widgets.append(pos)
                pos_inicial_x += w/2-margen_x
                
            pos_inicial_y+= 50 + espacio
                    
        #Crear boton home
        self.boton_home = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w - 45 ,
                                       y =  h - 45,
                                       w= 35,
                                       h = 35,
                                       path_image = r"UI\Recursos\home.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""
                                       )
        

        self.lista_widgets.append(self.boton_home)
        
    def btn_home_click(self,parametro):
        self.end_dialog()
    
    def update(self, lista_eventos):
        if self.active:
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
            
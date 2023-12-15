import pygame, sys
from modulos.configuracion import Configuracion
from UI.Forms.GUI_form_principal import FormPrincipal
from Personajes.Heroe import Heroe

pygame.init()    
                
config_inicial = Configuracion()
config_inicial.cargar_configuracion()

form_inicial = FormPrincipal(config_inicial.PANTALLA, 0, 0, config_inicial.PANTALLA.get_width()
                             , config_inicial.PANTALLA.get_height(), "cyan", "Black")

personaje_principal = Heroe((80,70), 30, 60 , 10) 

while True:
    eventos = pygame.event.get() 
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
            
    form_inicial.update(eventos, personaje_principal)
    
    pygame.display.update()
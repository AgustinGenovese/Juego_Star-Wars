import pygame
from assets.imagenes import *
from assets.sonidos import *
from Niveles.nivel import Nivel
from Personajes.Heroe import Heroe
from Personajes.Enemigo import Enemigo
from Objetos.plataformas import Plataforma
from Objetos.Puertas import Puertas 
from Objetos.items import Item
from Objetos.Trampas import Trampas

class NivelDos(Nivel):
    def __init__(self, pantalla: pygame.Surface):
            
            W = pantalla.get_width()
            H = pantalla.get_height()
            
            imagen_fondo = pygame.transform.scale(fondo_nivel_2, (W, H))
                    
            #Plataformas
            piso = Plataforma(False, (W,20), 0, 600)        
            plataforma_1 = Plataforma(True, (300,20), -80, 450, plataforma_nivel_2)
            plataforma_2 = Plataforma(True, (300,20), 300, 300, plataforma_nivel_2)
            plataforma_3 = Plataforma(True, (300,20), 700, 450, plataforma_nivel_2)
            plataforma_4 = Plataforma(True, (300,20), -80, 150, plataforma_nivel_2)        
            plataformas = [piso, plataforma_1, plataforma_2, plataforma_3, plataforma_4]
            
            #Enemigos
            un_enemigo = Enemigo(800, 382, plataforma_3, "Izquierda_n2", 2)
            segundo_enemigo = Enemigo(300, 230, plataforma_2, "Izquierda_n2", 2)
            lista_enemigos = [un_enemigo, segundo_enemigo ]
            
            #Puerta
            puerta_nivel_2 = Puertas(40, 70, "Puerta_n2", (120, 80))   
            
            trampa_cortadora = Trampas(180, 325, (80,80), "Giratoria")
            lista_trampa = [trampa_cortadora]
            
            item = Item(50, 385, (65,65), "Estrella")
            lista_items = [item]
            
            enemigo_final = None
            
            proximo_nivel = "Nivel_tres"
            
            super().__init__(pantalla, plataformas, lista_enemigos, lista_trampa, imagen_fondo, lista_items,
                              proximo_nivel, enemigo_final, puerta_nivel_2)
      
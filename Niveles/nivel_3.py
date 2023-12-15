import pygame
import random
from Objetos.Puertas import Puertas
from assets.imagenes import *
from assets.sonidos import *
from Niveles.nivel import Nivel
from Personajes.Enemigo import Enemigo
from Objetos.plataformas import Plataforma
from Personajes.Enemigo_final import Enemigo_Final
from Objetos.items import Item
from Objetos.Trampas import Trampas

class NivelTres(Nivel):
    def __init__(self, pantalla: pygame.Surface):

            W = pantalla.get_width()
            H = pantalla.get_height()
            
            imagen_fondo = pygame.transform.scale(fondo_nivel_3, (W, H))
                        
            #Plataformas
            piso = Plataforma(True, (W,50), 0, 600, plataforma_nivel_2)        
            plataforma_1 = Plataforma(True, (150,20), 35, 450, plataforma_nivel_2)
            plataforma_2 = Plataforma(True, (150,20), 300, 300, plataforma_nivel_2)
            plataforma_4 = Plataforma(True, (180,20), 0, 150, plataforma_nivel_2)        
            plataformas = [piso, plataforma_4, plataforma_1, plataforma_2 ]
            
            #Enemigos
            un_enemigo = Enemigo(20, 382, plataforma_1, "Izquierda_n2", 2)
            segundo_enemigo = Enemigo(300, 230, plataforma_2, "Izquierda_n1", 1)
            
            random_x_1 = random.randint(100, 400)
            random_x_2 = random.randint(400, 900)
            cuarto_enemigo_random = Enemigo(random_x_1, 0, piso, "Izquierda_n2", 2)
            quinto_enemigo_random = Enemigo(random_x_2, 0, piso, "Izquierda_n2", 2)
            lista_enemigos = [un_enemigo, segundo_enemigo, cuarto_enemigo_random, quinto_enemigo_random]
            
            enemigo_final = Enemigo_Final(W//1.72, H//2, "Halcon_milenario", pantalla)

            # Puerta
            puerta_nivel_fin = Puertas(40, 500, "Puerta_n2", (120, 80))
            
            #Trampa
            trampa_cortadora = Trampas(200, 150, (80,80), "Giratoria")
            lista_trampas = [trampa_cortadora]
            
            #Item
            item = Item(850, 520, (70,70), "Estrella")
            lista_items = [item]

            proximo_nivel = "Nivel_fin"
            
            super().__init__(pantalla, plataformas,lista_enemigos, lista_trampas, imagen_fondo, lista_items,
                             proximo_nivel, enemigo_final, puerta_nivel_fin)

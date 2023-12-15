from Niveles.nivel import Nivel
from Objetos.Puertas import Puertas
from Objetos.plataformas import Plataforma
from UI.GUI_button_image import *
from assets.imagenes import fondo_nivel_3, plataforma_nivel_2

class NivelFin(Nivel):
    def __init__(self, pantalla: pygame.Surface):
        W = pantalla.get_width()
        H = pantalla.get_height()

        imagen_fondo = pygame.transform.scale(fondo_nivel_3, (W, H))

        # Plataformas
        piso = Plataforma(True, (W, 50), 0, 600, plataforma_nivel_2)
        plataforma_1 = Plataforma(True, (150, 20), -200, -200, plataforma_nivel_2)
        plataforma_2 = Plataforma(True, (150, 20), -200, -200, plataforma_nivel_2)
        plataforma_4 = Plataforma(True, (150, 20), -200, -200, plataforma_nivel_2)
        plataformas = [piso, plataforma_1, plataforma_2, plataforma_4]

        # Puerta
        puerta_nivel_fin = Puertas(-200, -200, "Puerta_n2", (120, 80))

        super().__init__(pantalla,  plataformas, [], None, imagen_fondo, None,
                         None, None, puerta_nivel_fin)

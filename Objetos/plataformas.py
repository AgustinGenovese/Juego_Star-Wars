import pygame

class Plataforma():
    def __init__(self, esta_visible, tamaño,  x,  y, imagen = None ):
        self.esta_visible = esta_visible
        self.tamaño = tamaño
        self.ubicacion_x = x
        self.ubicacion_y = y
        self.superficie = imagen
        
        self.rect_superior = pygame.Rect(x, y , tamaño[0], 5)
        self.rect_inferior = pygame.Rect(x, y + 15, tamaño[0], 5)
        self.rect_izquierdo = pygame.Rect(x, y, 5, tamaño[1])
        self.rect_derecho = pygame.Rect(self.rect_superior.right -5 , y , 5, tamaño[1])
        
        self.diccionario_plataforma = self.crear_plataforma()
        self.diccionario_plataformas_int = self.crear_internas()
    
    def crear_plataforma(self):
        """
        Crea y devuelve el rectángulo de la plataforma con su superficie en caso que sea una plataforma visible
        """
        
        plataforma = {}
        if self.esta_visible:
            plataforma["superficie"] = pygame.transform.scale(self.superficie, self.tamaño)
        else:
            plataforma["superficie"] = pygame.Surface((self.tamaño[0], self.tamaño[1]))

        plataforma["rectangulo"] = plataforma["superficie"].get_rect()
        plataforma["rectangulo"].x = self.ubicacion_x
        plataforma["rectangulo"].y = self.ubicacion_y
        
        return plataforma
    
    def crear_internas(self):
        """
         Crea y devuelve un diccionario con los rectángulos internos de la plataforma.
        """
        
        diccionario = {}
        diccionario["superior"] = self.rect_superior
        diccionario["inferior"] = self.rect_inferior
        diccionario["izquierdo"] = self.rect_izquierdo
        diccionario["derecho"] = self.rect_derecho
        return diccionario
        
        
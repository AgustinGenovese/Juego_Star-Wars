import pygame

def reescalar_imagenes(diccionario_animaciones, ancho, alto):
    """
    Reescala las imágenes en un diccionario de animaciones a un nuevo ancho y alto.
    La función modifica el diccionario_animaciones directamente.
    Parameters:
        diccionario_animaciones (dict): Un diccionario que contiene listas de imágenes para cada animación.
        ancho (int): El nuevo ancho deseado para las imágenes.
        alto (int): El nuevo alto deseado para las imágenes.
    """
    for clave in diccionario_animaciones:
        for i in range(len(diccionario_animaciones[clave])):
            img = diccionario_animaciones[clave][i]
            diccionario_animaciones[clave][i] = pygame.transform.scale(img, (ancho,alto))

def play_sonido(sonidos, jugador, volumen = 0.2 ):
    """
    Reproduce un sonido si la propiedad de sonido del jugador está habilitada.
    Parameters:
        sonidos (str): La ruta al archivo de sonido que se reproducirá.
        jugador (objeto): El objeto del jugador que tiene una propiedad 'sonido'.
        volumen (float, optional): El volumen del sonido, con un valor predeterminado de 0.2.
    """
    if jugador.sonido:
        sonidos = pygame.mixer.Sound(sonidos)
        sonidos.set_volume(volumen)
        sonidos.play()

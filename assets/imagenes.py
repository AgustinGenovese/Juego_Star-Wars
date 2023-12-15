import pygame

#Personaje Principal
personaje_quieto_derecha = [pygame.image.load(r"assets\imagenes\01.png")]

personaje_quieto_izquierda = [pygame.image.load(r"assets\imagenes\03.png")]

personaje_camina_derecha = [pygame.image.load(r"assets\imagenes\01.png"),
                            pygame.image.load(r"assets\imagenes\02.png")]

personaje_camina_izquierda = [pygame.image.load(r"assets\imagenes\03.png"),
                            pygame.image.load(r"assets\imagenes\04.png")]

disparo_simple = pygame.image.load("assets\imagenes\disparo_p.png")

disparo_r2d2 = pygame.image.load("assets\imagenes\disparo.PNG")

icono = pygame.image.load("assets\imagenes\icono.png")

fondo_inicio = pygame.image.load(r"assets\imagenes\fondo_inicio.jpg")

explosion = [pygame.image.load(r"assets\imagenes\explocion.png")]

vida = [pygame.image.load(r"assets\imagenes\vida.png"),
        pygame.image.load(r"assets\imagenes\vida.png"),
        pygame.image.load(r"assets\imagenes\vida.png"),
        pygame.image.load(r"assets\imagenes\vida.png")]

item = [pygame.image.load(r"assets\imagenes\item2.png")]

#Nivel 1
fondo_nivel_1 = pygame.image.load(r"assets\imagenes\nivel_1\fondo_nivel_1.jpg")

plataforma_nivel_1 = pygame.image.load(r"assets\imagenes\nivel_1\plataformas_nivel_1.PNG")

enemigo_camina_izquierda_n1 = [pygame.image.load(r"assets\imagenes\nivel_1\ene.1.png"),
                          pygame.image.load(r"assets\imagenes\nivel_1\ene.1.png"),
                            pygame.image.load(r"assets\imagenes\nivel_1\ene.2.png"),
                            pygame.image.load(r"assets\imagenes\nivel_1\ene.2.png")
                            ]

enemigo_camina_derecha_n1 = [pygame.image.load(r"assets\imagenes\nivel_1\ene.1.reversa.png"),
                            pygame.image.load(r"assets\imagenes\nivel_1\ene.1.reversa.png"),
                            pygame.image.load(r"assets\imagenes\nivel_1\ene.2.reversa.png"),
                            pygame.image.load(r"assets\imagenes\nivel_1\ene.2.reversa.png")]


ard2_dorado = [pygame.image.load(r"assets\imagenes\nivel_1\r2d2.png")]

puerta_nivel_1 = [pygame.image.load(r"assets\imagenes\nivel_1\puerta_nivel_1.png"),
          pygame.image.load(r"assets\imagenes\nivel_1\puerta_nivel_1_abierta.png"),]

#Nivel 2
fondo_nivel_2 = pygame.image.load(r"assets\imagenes\nivel_2\fondo_nivel_2.jpg")

plataforma_nivel_2 = pygame.image.load(r"assets\imagenes\nivel_2\plataformas_nivel_2.PNG")

enemigo_camina_derecha_n2 = [pygame.image.load(r"assets\imagenes\nivel_2\ene.2.png"),
                          pygame.image.load(r"assets\imagenes\nivel_2\ene.2.png"),
                            pygame.image.load(r"assets\imagenes\nivel_2\ene.1.png"),
                            pygame.image.load(r"assets\imagenes\nivel_2\ene.1.png")
                            ]

enemigo_camina_izquierda_n2 = [pygame.image.load(r"assets\imagenes\nivel_2\ene.2.reversa.png"),
                            pygame.image.load(r"assets\imagenes\nivel_2\ene.2.reversa.png"),
                            pygame.image.load(r"assets\imagenes\nivel_2\ene.1.reversa.png"),
                            pygame.image.load(r"assets\imagenes\nivel_2\ene.1.reversa.png")]

ard2_plateado = [pygame.image.load(r"assets\imagenes\nivel_2\r2d2.png")
               ]

puerta_nivel_2 = [pygame.image.load(r"assets\imagenes\nivel_2\puerta_nivel_2.png"),
          pygame.image.load(r"assets\imagenes\nivel_2\puerta_nivel_2_abierta.png"),]


#Nivel 3 
fondo_nivel_3 = pygame.image.load(r"assets\imagenes\nivel_3\fondo_nivel_3.PNG")

enemigo_final = [pygame.image.load(r"assets\imagenes\nivel_3\halcon_milenario.png")]

trampa_cortadora = [pygame.image.load(r"assets\imagenes\trampa.PNG")]

explosion = [pygame.image.load(r"assets\imagenes\Explo.png"),
             pygame.image.load(r"assets\imagenes\Explo.png"),
             pygame.image.load(r"assets\imagenes\Explo.png"),
             pygame.image.load(r"assets\imagenes\Explo.png"),
             pygame.image.load(r"assets\imagenes\Explo.png"),
             pygame.image.load(r"assets\imagenes\Explo.png"),
             pygame.image.load(r"assets\imagenes\Explo.png"),
             ]
from Niveles.nivel_1 import NivelUno
from Niveles.nivel_2 import NivelDos
from Niveles.nivel_3 import NivelTres
from Niveles.nivel_fin import NivelFin


class Manejador_niveles:
    def __init__(self, pantalla):
        self.slave = pantalla
        self.niveles = {"Nivel_uno": NivelUno, "Nivel_dos": NivelDos, "Nivel_tres": NivelTres, "Nivel_fin": NivelFin}

    def get_nivel(self, nombre_nivel):
        """
        Obtiene una instancia del nivel correspondiente según el nombre proporcionado.
        
        Parameters: nombre_nivel (str): El nombre del nivel deseado.
        Returns:: objeto: Una instancia del nivel correspondiente.

        """
        return self.niveles[nombre_nivel](self.slave)
        #NivelUno(pantalla)
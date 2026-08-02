import pygame
import random
import sys

pygame.init()

ANCHO_VENTANA = 600
ALTO_VENTANA = 600
TAM_BLOQUE = 30
ANCHO_BLOQUES = ANCHO_VENTANA // TAM_BLOQUE
ALTO_BLOQUES = ALTO_VENTANA // TAM_BLOQUE
FPS = 10


NEGRO = (0, 0, 0)
NARANJA = (128, 0, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 150, 0)
AZUL = (0, 0, 255)

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Snake - Aprende programando")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont(None, 40)
fuente_peque = pygame.font.SysFont(None, 28)


class Serpiente:
    def __init__(self):
        self.cuerpo = [
            (ANCHO_BLOQUES // 2, ALTO_BLOQUES // 2),
            (ANCHO_BLOQUES // 2 - 1, ALTO_BLOQUES // 2),
            (ANCHO_BLOQUES // 2 - 2, ALTO_BLOQUES // 2),
        ]
        self.direccion = (1, 0)
        self.nueva_direccion = (1, 0)
        self.crecer = False

    def cambiar_direccion(self, dx, dy):
        if self.direccion[0] + dx == 0 and self.direccion[1] + dy == 0:
            return
        self.nueva_direccion = (dx, dy)

    def mover(self):
        self.direccion = self.nueva_direccion
        cabeza_x, cabeza_y = self.cuerpo[0]
        nueva_cabeza = (cabeza_x + self.direccion[0], cabeza_y + self.direccion[1])
        self.cuerpo.insert(0, nueva_cabeza)
        if self.crecer:
            self.crecer = False
        else:
            self.cuerpo.pop()

    def dibujar(self):
        for i, (x, y) in enumerate(self.cuerpo):
            rect = pygame.Rect(
                x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE - 1, TAM_BLOQUE - 1
            )
            if i == 0:
                pygame.draw.rect(ventana, VERDE, rect)
                ojo_1 = pygame.Rect(
                    x * TAM_BLOQUE + 5, y * TAM_BLOQUE + 5, 6, 6
                )
                ojo_2 = pygame.Rect(
                    x * TAM_BLOQUE + TAM_BLOQUE - 11, y * TAM_BLOQUE + 5, 6, 6
                )
                pygame.draw.rect(ventana, NEGRO, ojo_1)
                pygame.draw.rect(ventana, NEGRO, ojo_2)
            else:
                pygame.draw.rect(ventana, VERDE_OSCURO, rect)


class Comida:
    def __init__(self, serpiente):
        self.posicion = self.generar_posicion(serpiente)

    def generar_posicion(self, serpiente):
        while True:
            x = random.randint(0, ANCHO_BLOQUES - 1)
            y = random.randint(0, ALTO_BLOQUES - 1)
            if (x, y) not in serpiente.cuerpo:
                return (x, y)

    def dibujar(self):
        x, y = self.posicion
        rect = pygame.Rect(
            x * TAM_BLOQUE + 2, y * TAM_BLOQUE + 2, TAM_BLOQUE - 5, TAM_BLOQUE - 5
        )
        pygame.draw.rect(ventana, ROJO, rect, border_radius=8)


def dibujar_texto(texto, color, x, y, fuente_uso=fuente):
    superficie = fuente_uso.render(texto, True, color)
    ventana.blit(superficie, (x, y))


def colision_paredes(serpiente):
    cabeza_x, cabeza_y = serpiente.cuerpo[0]
    return cabeza_x < 0 or cabeza_x >= ANCHO_BLOQUES or cabeza_y < 0 or cabeza_y >= ALTO_BLOQUES


def colision_cuerpo(serpiente):
    cabeza = serpiente.cuerpo[0]
    return cabeza in serpiente.cuerpo[1:]


def colision_comida(serpiente, comida):
    return serpiente.cuerpo[0] == comida.posicion
    


def reiniciar_juego():
    serpiente = Serpiente()
    comida = Comida(serpiente)
    velocidad_actual = FPS
    contador_comidas = 0
    return serpiente, comida, 0, velocidad_actual, contador_comidas


def bucle_principal():
    serpiente, comida, puntuacion, velocidad_actual, contador_comidas = reiniciar_juego()
    en_juego = True
    game_over = False
    velocidad_actual = FPS
    contador_comidas = 0
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if game_over:
                    if evento.key == pygame.K_r:
                        serpiente, comida, puntuacion, velocidad_actual, contador_comidas = reiniciar_juego()
                        game_over = False
                        en_juego = True
                    elif evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif en_juego:
                    if evento.key == pygame.K_UP:
                        serpiente.cambiar_direccion(0, -1)
                    elif evento.key == pygame.K_DOWN:
                        serpiente.cambiar_direccion(0, 1)
                    elif evento.key == pygame.K_LEFT:
                        serpiente.cambiar_direccion(-1, 0)
                    elif evento.key == pygame.K_RIGHT:
                        serpiente.cambiar_direccion(1, 0)

        if en_juego and not game_over:
            serpiente.mover()

            if colision_paredes(serpiente) or colision_cuerpo(serpiente):
                game_over = True

            if colision_comida(serpiente, comida):
                serpiente.crecer = True
                puntuacion += 10
                contador_comidas += 1
                if contador_comidas % 5 == 0:
                    velocidad_actual += 2
                comida = Comida(serpiente)

        ventana.fill(NEGRO)

        for x in range(ANCHO_BLOQUES):
            for y in range(ALTO_BLOQUES):
                if (x + y) % 2 == 0:
                    rect = pygame.Rect(
                        x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE
                    )
                    pygame.draw.rect(ventana, (20, 20, 20), rect)

        serpiente.dibujar()
        comida.dibujar()

        dibujar_texto(f"Puntos: {puntuacion}", NARANJA, 10, 10, fuente_peque)
        dibujar_texto(f"Velocidad: {velocidad_actual}", NARANJA, ANCHO_VENTANA - 180, 10, fuente_peque)

        if game_over:
            rect_go = pygame.Rect(
                ANCHO_VENTANA // 2 - 200, ALTO_VENTANA // 2 - 80, 400, 160
            )
            pygame.draw.rect(ventana, AZUL, rect_go, border_radius=15)
            dibujar_texto("GAME OVER", ROJO, ANCHO_VENTANA // 2 - 85, ALTO_VENTANA // 2 - 50)
            dibujar_texto(
                f"Puntos: {puntuacion}",
                NARANJA,
                ANCHO_VENTANA // 2 - 55,
                ALTO_VENTANA // 2,
                fuente_peque,
            )
            dibujar_texto(
                "R = Reiniciar | Q = Salir",
                NARANJA,
                ANCHO_VENTANA // 2 - 150,
                ALTO_VENTANA // 2 + 35,
                fuente_peque,
            )

        pygame.display.flip()
        reloj.tick(velocidad_actual)


if __name__ == "__main__":
    bucle_principal()

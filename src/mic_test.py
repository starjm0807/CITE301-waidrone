import sys
from multiprocessing import Process
from multiprocessing import Manager

import pygame

import Mic
from Packet import Coor


def pygame_mic_test(d_coordinate):
    # pygame parameters
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # prepare pygame window
    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)
    font = pygame.font.SysFont("freesansbold", 30)

    # main loop
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        # print("pygame : {}".format(d_coordinate.value))
        coordinate = d_coordinate.value
        text = font.render(coordinate.__str__(), True, BLACK, WHITE)
        screen.blit(text, (0, 0))

        if coordinate is not None:
            if coordinate.activity > 0.7:
                if coordinate.x > 0.4:  # North
                    text2 = font.render("North  ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                elif coordinate.x < -0.4:  # South
                    text2 = font.render("South  ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                else:
                    text2 = font.render("           ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                if coordinate.y > 0.4:  # West
                    text3 = font.render("West   ", True, BLACK, WHITE)
                    screen.blit(text3, (0, 100))
                elif coordinate.y < -0.4:  # East
                    text3 = font.render("East   ", True, BLACK, WHITE)
                    screen.blit(text3, (0, 100))
                else:
                    text3 = font.render("            ", True, BLACK, WHITE)
                    screen.blit(text3, (0, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    # HACK: use lock to prevent race condition
    d_coordinate = Manager().Value(Coor, None)
    proc = Process(target=pygame_mic_test, args=(d_coordinate,))
    proc.start()
    Mic.init(d_coordinate)

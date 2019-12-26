import math
import sys
import time
from multiprocessing import Process

import pygame
from pyparrot.Bebop import Bebop


def init(d_coordinate, func):
    process = Process(target=func, args=(d_coordinate,))
    process.start()


def __drone_init():
    # prepare bebop drone
    bebop = Bebop()
    print("connecting ...")
    success = bebop.connect(5)
    if not success:
        sys.exit(1)

    bebop.ask_for_state_update()

    bebop.safe_takeoff(5)
    bebop.set_max_tilt(5)
    bebop.set_max_vertical_speed(1)
    bebop.set_hull_protection(1)

    bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=10, duration=2)
    bebop.smart_sleep(4)

    return bebop


def __drone_fin(bebop):
    bebop.safe_land(5)
    bebop.disconnect()


def aud_wasd(d_coordinate):
    # pygame parameters
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # prepare pygame window
    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)
    font = pygame.font.SysFont("freesansbold", 30)

    # prepare drone
    bebop = __drone_init()

    # main loop
    clock = pygame.time.Clock()
    done = False
    while not done:
        clock.tick(60)
        bebop.smart_sleep(0.01)

        # print coordinate on pygame window
        coordinate = d_coordinate.value
        text = font.render(coordinate.__str__(), True, BLACK, WHITE)
        screen.blit(text, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.update()

        # WASD motion
        roll = 0
        pitch = 0
        yaw = 0
        vertical = 0
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_w]:
            pitch += 20
        if key_event[pygame.K_s]:
            pitch -= 20
        if key_event[pygame.K_a]:
            roll -= 20
        if key_event[pygame.K_d]:
            roll += 20
        if key_event[pygame.K_q]:
            yaw += 40
        if key_event[pygame.K_e]:
            yaw -= 40
        if key_event[pygame.K_r]:
            vertical += 10
        if key_event[pygame.K_f]:
            vertical -= 10
        bebop.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=0.01)

        # escape condition
        if key_event[pygame.K_ESCAPE]:
            break

    pygame.quit()

    __drone_fin(bebop)


def aud_track_basic(d_coordinate):
    # pygame parameters
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # prepare pygame window
    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)
    font = pygame.font.SysFont("freesansbold", 30)

    # prepare drone
    bebop = __drone_init()
    print(bebop.sensors.battery)

    # mic control
    clock = pygame.time.Clock()
    done = False
    while not done:
        # clock.tick(10)
        clock.tick(60)

        # print coordinate on pygame window
        coordinate = d_coordinate.value
        text = font.render(coordinate.__str__(), True, BLACK, WHITE)
        screen.blit(text, (0, 0))

        # drone control
        roll = 0
        pitch = 0
        yaw = 0
        vertical = 0
        MIC_THRESHOLD = 0.1
        DRONE_VEL = 20 / (1 - MIC_THRESHOLD)
        if coordinate is not None:
            if coordinate.activity > 0.9:
                if coordinate.x > MIC_THRESHOLD:  # North
                    # print direction
                    text2 = font.render("North  ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                    # control drone
                    pitch -= DRONE_VEL * abs(coordinate.x - MIC_THRESHOLD)
                elif coordinate.x < -MIC_THRESHOLD:  # South
                    # print direction
                    text2 = font.render("South  ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                    # control drone
                    pitch += DRONE_VEL * abs(coordinate.x - MIC_THRESHOLD)
                else:
                    # print direction
                    text2 = font.render("       ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                if coordinate.y > MIC_THRESHOLD:  # West
                    # print direction
                    text3 = font.render("West   ", True, BLACK, WHITE)
                    screen.blit(text3, (100, 50))
                    # control drone
                    roll += DRONE_VEL * abs(coordinate.x - MIC_THRESHOLD)
                elif coordinate.y < -MIC_THRESHOLD:  # East
                    # print direction
                    text3 = font.render("East   ", True, BLACK, WHITE)
                    screen.blit(text3, (100, 50))
                    # control drone
                    roll -= DRONE_VEL * abs(coordinate.x - MIC_THRESHOLD)
                else:
                    text3 = font.render("       ", True, BLACK, WHITE)
                    screen.blit(text3, (100, 50))

        if roll == 0 and pitch == 0 and yaw == 0 and vertical == 0:
            bebop.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=0.1)
            # bebop.move_relative(0, 0, 0, math.radians(0))
            # print(bebop.sensors.RelativeMoveEnded)
            text4 = font.render("stop    ", True, BLACK, WHITE)
            screen.blit(text4, (0, 100))
        else:
            bebop.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=0.1)
            text4 = font.render("move    ", True, BLACK, WHITE)
            screen.blit(text4, (0, 100))

        # quit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_ESCAPE]:
            done = True

        pygame.display.update()

    pygame.quit()

    __drone_fin(bebop)


def aud_track_advanced(d_coordinate):
    # pygame parameters
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # prepare pygame window
    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)
    font = pygame.font.SysFont("freesansbold", 30)

    # prepare drone
    bebop = __drone_init()
    print(bebop.sensors.battery)

    # mic control
    clock = pygame.time.Clock()
    done = False
    while not done:
        # clock.tick(10)
        clock.tick(60)

        # print coordinate on pygame window
        coordinate = d_coordinate.value
        text = font.render(coordinate.__str__(), True, BLACK, WHITE)
        screen.blit(text, (0, 0))

        # drone control
        roll = 0
        pitch = 0
        yaw = 0
        vertical = 0
        MIC_THRESHOLD = 0.2
        DRONE_VEL = 10
        if coordinate is not None:
            if coordinate.activity > 0.7:
                if coordinate.x > MIC_THRESHOLD:  # North
                    # print direction
                    text2 = font.render("North  ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                    # control drone
                    pitch -= DRONE_VEL
                elif coordinate.x < -MIC_THRESHOLD:  # South
                    # print direction
                    text2 = font.render("South  ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                    # control drone
                    pitch += DRONE_VEL
                else:
                    # print direction
                    text2 = font.render("       ", True, BLACK, WHITE)
                    screen.blit(text2, (0, 50))
                if coordinate.y > MIC_THRESHOLD:  # West
                    # print direction
                    text3 = font.render("West   ", True, BLACK, WHITE)
                    screen.blit(text3, (100, 50))
                    # control drone
                    roll += DRONE_VEL
                elif coordinate.y < -MIC_THRESHOLD:  # East
                    # print direction
                    text3 = font.render("East   ", True, BLACK, WHITE)
                    screen.blit(text3, (100, 50))
                    # control drone
                    roll -= DRONE_VEL
                else:
                    text3 = font.render("       ", True, BLACK, WHITE)
                    screen.blit(text3, (100, 50))

        if roll == 0 and pitch == 0 and yaw == 0 and vertical == 0:
            bebop.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=0.01)
            text4 = font.render("stop    ", True, BLACK, WHITE)
            screen.blit(text4, (0, 100))
        else:
            bebop.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=0.01)
            text4 = font.render("move    ", True, BLACK, WHITE)
            screen.blit(text4, (0, 100))

        # quit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_ESCAPE]:
            done = True

        pygame.display.update()

    pygame.quit()

    __drone_fin(bebop)

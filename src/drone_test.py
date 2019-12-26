import math
import sys

import pygame
from pyparrot.Bebop import Bebop


def connection_test():
    bebop = Bebop()

    print("connecting")
    success = bebop.connect(10)
    print(success)
    if not success:
        sys.exit(1)

    bebop.ask_for_state_update()

    bebop.smart_sleep(5)
    print(bebop.sensors.battery)
    bebop.disconnect()


def relative_test():
    bebop = Bebop()

    print("connecting")
    success = bebop.connect(10)
    print(success)

    bebop.ask_for_state_update()

    # take off
    bebop.safe_takeoff(10)
    bebop.smart_sleep(5)

    # relative
    bebop.move_relative(0, 0.3, 0, math.radians(0))

    # land
    bebop.safe_land(10)

    print("DONE - disconnecting")
    bebop.disconnect()


def pygame_connection_test():
    # prepare bebop drone
    bebop = Bebop()

    print("connecting ...")
    success = bebop.connect(5)

    if success:
        print("connection success")
    else:
        print("connection failed")
        sys.exit(1)

    print("sleeping")
    bebop.smart_sleep(5)
    bebop.ask_for_state_update()

    # prepare pygame window
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    white = (255, 255, 255)
    black = (0, 0, 0)

    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(black)
    clock = pygame.time.Clock()

    # main loop
    done = False
    while not done:
        bebop.smart_sleep(0.01)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_ESCAPE]:
            break

    bebop.disconnect()


def takeoff_test():
    bebop = Bebop()

    print("connecting")
    success = bebop.connect(10)
    print(success)

    bebop.ask_for_state_update()

    # take off
    bebop.safe_takeoff(10)
    bebop.smart_sleep(5)

    print("DONE - disconnecting")
    bebop.disconnect()


def land_test():
    bebop = Bebop()

    print("connecting")
    success = bebop.connect(10)
    print(success)

    # print("sleeping")
    # bebop.smart_sleep(5)
    bebop.ask_for_state_update()
    # HACK: fix sensor packet error

    # land
    bebop.safe_land(10)

    print("DONE - disconnecting")
    bebop.disconnect()


def takeoff_land_test():
    bebop = Bebop()

    print("connecting")
    success = bebop.connect(10)
    print(success)
    if not success:
        sys.exit(1)

    bebop.ask_for_state_update()

    # take off
    bebop.safe_takeoff(10)
    bebop.smart_sleep(5)

    # land
    bebop.safe_land(10)

    print("DONE - disconnecting")
    bebop.disconnect()


def flip_test():
    bebop = Bebop()

    print("connecting")
    success = bebop.connect(10)
    print(success)

    print("sleeping")
    bebop.smart_sleep(5)

    bebop.ask_for_state_update()

    bebop.safe_takeoff(10)

    print("flip left")
    print("flying state is %s" % bebop.sensors.flying_state)
    success = bebop.flip(direction="left")
    print("mambo flip result %s" % success)
    bebop.smart_sleep(5)

    bebop.smart_sleep(5)
    bebop.safe_land(10)

    print("DONE - disconnecting")
    bebop.disconnect()


def wasd_relative_test():
    # prepare bebop drone
    bebop = Bebop()

    print("connecting ...")
    success = bebop.connect(5)

    if success:
        print("connection success")
    else:
        print("connection failed")
        sys.exit(1)

    print("sleeping")
    bebop.smart_sleep(5)
    bebop.ask_for_state_update()

    bebop.safe_takeoff(10)
    bebop.set_max_tilt(5)
    bebop.set_max_vertical_speed(1)
    bebop.set_hull_protection(1)

    # prepare pygame window
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    clock = pygame.time.Clock()

    # main loop
    done = False
    while not done:
        bebop.smart_sleep(0.01)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        x = 0.0
        y = 0.0
        z = 0.0
        angle = 0.0
        THREASHOLD = 0.1
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_w]:
            x += THREASHOLD
        if key_event[pygame.K_s]:
            x -= THREASHOLD
        if key_event[pygame.K_a]:
            y -= THREASHOLD
        if key_event[pygame.K_d]:
            y += THREASHOLD
        if key_event[pygame.K_q]:
            angle -= 200 * THREASHOLD
        if key_event[pygame.K_e]:
            angle += 200 * THREASHOLD
        if key_event[pygame.K_r]:
            z += THREASHOLD
        if key_event[pygame.K_f]:
            z -= THREASHOLD
        # bebop.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=0.01)
        bebop.move_relative(x, y, z, math.radians(angle))

        if key_event[pygame.K_ESCAPE]:
            break

    print("DONE - landing ...")
    bebop.safe_land(5)
    print("landed ...")

    print("disconnecting ...")
    bebop.disconnect()
    print("disconnected")


def wasd_direct_test():
    # prepare bebop drone
    bebop = Bebop()

    print("connecting ...")
    success = bebop.connect(5)

    if success:
        print("connection success")
    else:
        print("connection failed")
        sys.exit(1)

    print("sleeping")
    bebop.smart_sleep(5)
    bebop.ask_for_state_update()

    bebop.safe_takeoff(10)
    bebop.set_max_tilt(5)
    bebop.set_max_vertical_speed(1)
    bebop.set_hull_protection(1)

    # prepare pygame window
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    white = (255, 255, 255)
    black = (0, 0, 0)

    pygame.init()
    pygame.display.set_caption("waiDrone")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(black)
    clock = pygame.time.Clock()

    # main loop
    done = False
    while not done:
        bebop.smart_sleep(0.01)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_w]:
            bebop.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=0.01)
        elif key_event[pygame.K_s]:
            bebop.fly_direct(roll=0, pitch=-20, yaw=0, vertical_movement=0, duration=0.01)
        elif key_event[pygame.K_a]:
            bebop.fly_direct(roll=-20, pitch=0, yaw=0, vertical_movement=0, duration=0.01)
        elif key_event[pygame.K_d]:
            bebop.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=0.01)
        elif key_event[pygame.K_q]:
            bebop.fly_direct(roll=0, pitch=0, yaw=40, vertical_movement=0, duration=0.01)
        elif key_event[pygame.K_e]:
            bebop.fly_direct(roll=0, pitch=0, yaw=-40, vertical_movement=0, duration=0.01)
        elif key_event[pygame.K_r]:
            bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=10, duration=0.01)
        elif key_event[pygame.K_f]:
            bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-10, duration=0.01)

        if key_event[pygame.K_ESCAPE]:
            break

    print("DONE - landing ...")
    bebop.safe_land(5)
    print("landed ...")

    print("disconnecting ...")
    bebop.disconnect()
    print("disconnected")


if __name__ == '__main__':
    land_test()
    # connection_test()

# RandomMine pygame file
import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN

Display_width = 1200
Display_height = 800

Surface_width = 1200
Surface_height = 800

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

FPS = 40

pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

# Rock
Rock_rect = Rect(0, 0, 336, 231)
Rock_rect.center = (Surface_width / 2, Surface_height / 2)

Rock_image = pygame.transform.scale(pygame.image.load("resources/Rock.png"), Rock_rect.size)

rock_vibration_power = 10
rock_vibration_delay = 50


def main():
    tickTime = 1000 / FPS
    vibrationTick = 0

    CHANNEL = "MINE"

    while True:

        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            # exit code
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

            # event mouse position set
            elif pygame_event.type == MOUSEBUTTONDOWN:
                event_pos = (pygame_event.pos[0] / display_ratio_x,
                             pygame_event.pos[1] / display_ratio_y)

                if CHANNEL == "MINE":  # MOUSEBUTTONDOWN - MINE

                    # mining
                    if Rock_rect.collidepoint(event_pos):
                        vibrationTick = rock_vibration_delay

        # surface set
        SURFACE.fill((255, 0, 0))

        if CHANNEL == "MINE":
            # rock vibration
            if vibrationTick:
                SURFACE.blit(Rock_image, (Rock_rect.left + rock_vibration_power, Rock_rect.top))
                vibrationTick = max(vibrationTick - tickTime, 0)
            else:
                SURFACE.blit(Rock_image, Rock_rect.topleft)

        # system
        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        tickTime = FPSCLOCK.get_time()


if __name__ == "__main__":
    main()

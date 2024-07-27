# RandomMine pygame file
import pygame
import sys
from pygame.locals import QUIT, Rect

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
Rock_rect = Rect(0, 0, 394, 264)
Rock_rect.center = (Surface_width / 2, Surface_height / 2)

Rock_image = pygame.transform.scale(pygame.image.load("resources/Rock.png"), Rock_rect.size)


def main():
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 0, 0))

        SURFACE.blit(Rock_image, Rock_rect.topleft)

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()

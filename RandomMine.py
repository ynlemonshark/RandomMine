# RandomMine pygame file
import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN
from random import randint

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

# mineral
minerals = ("stone", "coal", "iron", "copper", "zinc", "silver", "gold", "bismuth")
mineral_chances = (600, 200, 100, 60, 30, 5, 4, 1)

mineral_chance_max = 0
for e_chance in mineral_chances:
    mineral_chance_max += e_chance

mineral_size = (64, 64)

mineral_images = pygame.transform.scale(pygame.image.load("resources/minerals.png"),
                                        (mineral_size[0] * len(minerals), mineral_size[1]))


class Mineral:
    def __init__(self, sort):
        self.sort = sort
        self.pos = Rock_rect.center

    def draw(self):
        SURFACE.blit(mineral_images, (self.pos[0] - mineral_size[0] / 2, self.pos[1] - mineral_size[1] / 2),
                     (mineral_size[0] * self.sort, 0, mineral_size[0], mineral_size[1]))


def main():
    tickTime = 1000 / FPS
    vibrationTick = 0

    CHANNEL = "MINE"

    MINERALS = []

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

                    if pygame_event.button == 1:
                       # mining
                        if Rock_rect.collidepoint(event_pos):
                            vibrationTick = rock_vibration_delay

                            # make mineral
                            ew_sort = 0
                            for ew_count in range(1):
                                ew_chance = randint(1, mineral_chance_max)
                                print(ew_chance)
                                for ew_mineral in range(len(minerals)):
                                    if ew_chance <= mineral_chances[ew_mineral]:
                                        ew_sort = ew_mineral
                                        break
                                    else:
                                        ew_chance -= mineral_chances[ew_mineral]
                                MINERALS.append(Mineral(ew_sort))


        # surface set
        SURFACE.fill((255, 0, 0))

        # CHANNEL - MINE
        if CHANNEL == "MINE":
            # rock vibration
            if vibrationTick:
                SURFACE.blit(Rock_image, (Rock_rect.left + rock_vibration_power, Rock_rect.top))
                vibrationTick = max(vibrationTick - tickTime, 0)
            else:
                SURFACE.blit(Rock_image, Rock_rect.topleft)

            # mineral draw
            for ew_index in range(len(MINERALS)):
                MINERALS[ew_index].draw()

        # SYSTEM
        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        tickTime = FPSCLOCK.get_time()


if __name__ == "__main__":
    main()

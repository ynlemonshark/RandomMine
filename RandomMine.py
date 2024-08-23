# RandomMine pygame file
import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN
from random import randint
from math import sin, cos, radians, dist

Display_width = 1200
Display_height = 800

Surface_width = 1200
Surface_height = 800

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

number_font = "IMPACT"
letter_font = "Calibri"

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
mineral_chances = (620, 220, 100, 30, 20, 5, 4, 1)
mineral_colors = ((127, 127, 127), (31, 31, 31), (191, 191, 191), (255, 127, 95), (127, 191, 191), (210, 210, 210),
                  (255, 191, 0), (191, 31, 191))

mineral_chain_decrease_chances = (5, 5, 4, 4, 5, 4, 4, 10)
mineral_chain_start_chances = (100, 90, 80, 80, 75, 70, 70, 70)

mineral_chance_max = 0
for e_chance in mineral_chances:
    mineral_chance_max += e_chance

mineral_size = (64, 64)

mineral_images = pygame.transform.scale(pygame.image.load("resources/minerals.png"),
                                        (mineral_size[0] * len(minerals), mineral_size[1]))

mineral_min_angle = 70
mineral_max_angle = 110

mineral_min_power = 700
mineral_max_power = 800

mineral_gravity = 1400

mineral_floor = 600

mineral_pickable_distance = 40

# inventory
inventory_button_rect = Rect(1000, 600, 200, 200)
inventory_button_image = pygame.transform.scale(pygame.image.load("resources/inventory_button.png"),
                                                inventory_button_rect.size)

inventory_mineral_size = (64, 64)
inventory_mineral_image = pygame.transform.scale(pygame.image.load("resources/minerals.png"),
                                                 (inventory_mineral_size[0] * len(minerals), inventory_mineral_size[1]))

inventory_mineral_first_topleft = (900, 120)
inventory_mineral_distance = 80

inventory_mineral_count_font = pygame.font.SysFont(number_font, 50, False, False)
inventory_mineral_count_text_space = 10

inventory_back_button_rect = Rect(0, 0, 75, 75)
inventory_back_button_image = pygame.transform.scale(pygame.image.load("resources/back button.png"),
                                                     inventory_back_button_rect.size)

inventory_mineral_frame_rect = Rect(850, 25, 300, 750)
inventory_mineral_frame_image = pygame.transform.scale(pygame.image.load("resources/mineral_frame.png"),
                                                       inventory_mineral_frame_rect.size)

# fatigue
fatigue_bar_rect = Rect(200, 700, 800, 100)
fatigue_bar_image = pygame.transform.scale(pygame.image.load("resources/fatigue_bar.png"), fatigue_bar_rect.size)

# background
background_channels = ("MINE", "INVENTORY")
background_images = {}
for e_channel in background_channels:
    background_images[e_channel] = pygame.transform.scale(
        pygame.image.load("resources/backgrounds/{}.png".format(e_channel)), (Surface_width, Surface_height))


class Mineral:
    def __init__(self, sort, angle, power):
        self.sort = sort
        self.pos = Rock_rect.center

        self.x_force = power * cos(radians(angle))
        self.y_force = power * sin(radians(angle))

        self.on_floor = False

    def tick(self, time):
        if not self.on_floor:
            self.y_force -= mineral_gravity * time / 1000
            self.pos = (self.pos[0] + self.x_force * time / 1000, self.pos[1] - self.y_force * time / 1000)
            if self.pos[1] > mineral_floor:
                self.pos = (self.pos[0], mineral_floor)
                self.on_floor = True

    def draw(self):
        SURFACE.blit(mineral_images, (self.pos[0] - mineral_size[0] / 2, self.pos[1] - mineral_size[1] / 2),
                     (mineral_size[0] * self.sort, 0, mineral_size[0], mineral_size[1]))


def main():
    tickTime = 1000 / FPS
    vibrationTick = 0

    CHANNEL = "MINE"

    MINERALS = []

    INVENTORY_MINERAL = []
    for em_repeat in range(len(minerals)):
        INVENTORY_MINERAL.append(0)

    CHAIN_MINERAL = 0
    CHAIN_PERCENT = 0

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
                        # inventory button click
                        if inventory_button_rect.collidepoint(event_pos):
                            CHANNEL = "INVENTORY"

                        # mining
                        if Rock_rect.collidepoint(event_pos):
                            vibrationTick = rock_vibration_delay

                            # make mineral
                            for ew_count in range(1):
                                if randint(1, 100) > CHAIN_PERCENT:
                                    CHAIN_MINERAL = 0
                                    ew_chance = randint(1, mineral_chance_max)
                                    for ew_mineral in range(len(minerals)):
                                        if ew_chance <= mineral_chances[ew_mineral]:
                                            CHAIN_MINERAL = ew_mineral
                                            break
                                        else:
                                            ew_chance -= mineral_chances[ew_mineral]

                                    CHAIN_PERCENT = mineral_chain_start_chances[CHAIN_MINERAL]
                                else:
                                    CHAIN_PERCENT -= mineral_chain_decrease_chances[CHAIN_MINERAL]

                                ew_sort = CHAIN_MINERAL

                                ew_angle = randint(mineral_min_angle, mineral_max_angle)
                                ew_power = randint(mineral_min_power, mineral_max_power)

                                MINERALS.append(Mineral(ew_sort, ew_angle, ew_power))

                        # pick up code
                        else:
                            for ew_index in range(len(MINERALS)):
                                if MINERALS[ew_index].on_floor:
                                    if mineral_pickable_distance >= dist(MINERALS[ew_index].pos, event_pos):
                                        INVENTORY_MINERAL[MINERALS[ew_index].sort] += 1
                                        MINERALS[ew_index] = 0

                            for ew_repeat in range(MINERALS.count(0)):
                                MINERALS.remove(0)

                elif CHANNEL == "INVENTORY":
                    if inventory_back_button_rect.collidepoint(event_pos):
                        CHANNEL = "MINE"


        # surface backgrounds
        SURFACE.blit(background_images[CHANNEL], (0, 0))

        # CHANNEL - MINE
        if CHANNEL == "MINE":
            # rock vibration
            if vibrationTick:
                SURFACE.blit(Rock_image, (Rock_rect.left + rock_vibration_power, Rock_rect.top))
                vibrationTick = max(vibrationTick - tickTime, 0)
            else:
                SURFACE.blit(Rock_image, Rock_rect.topleft)

            # mineral code
            for ew_index in range(len(MINERALS)):
                MINERALS[ew_index].tick(tickTime)

            # mineral draw
            for ew_index in range(len(MINERALS)):
                MINERALS[ew_index].draw()

            # fatigue bar draw
            SURFACE.blit(fatigue_bar_image, fatigue_bar_rect.topleft)

            # inventory button
            SURFACE.blit(inventory_button_image, inventory_button_rect.topleft)

        # CHANNEL - INVENTORY
        elif CHANNEL == "INVENTORY":
            # inventory draw mineral
            SURFACE.blit(inventory_mineral_frame_image, inventory_mineral_frame_rect.topleft)

            for ew_index in range(len(minerals)):
                SURFACE.blit(inventory_mineral_image,
                             (inventory_mineral_first_topleft[0],
                              inventory_mineral_first_topleft[1] + inventory_mineral_distance * ew_index),
                             (inventory_mineral_size[0] * ew_index, 0,
                              inventory_mineral_size[0], inventory_mineral_size[1]))
                ew_text = inventory_mineral_count_font.render(str(INVENTORY_MINERAL[ew_index]), True, mineral_colors[ew_index])
                ew_rect = ew_text.get_rect()
                ew_rect.midleft = (inventory_mineral_first_topleft[0] + inventory_mineral_size[0] +
                                  inventory_mineral_count_text_space, inventory_mineral_first_topleft[1] +
                                  inventory_mineral_distance * ew_index + inventory_mineral_size[1] / 2)

                SURFACE.blit(ew_text, ew_rect.topleft)

            SURFACE.blit(inventory_back_button_image, inventory_back_button_rect.topleft)


        # SYSTEM
        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        tickTime = FPSCLOCK.get_time()


if __name__ == "__main__":
    main()

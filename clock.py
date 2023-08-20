#!/usr/bin/env python3

import pygame
import pygame.freetype
import datetime
import math

# need to know what time it is

# show the display
# tachometer on the left side for RPM / hour
# big speedometer in the center
# fuel gauge shows the battery percentage

# find a way to draw the clock
# draw each subcomponent
# done

def main():
    pygame.init()

    #load = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("RPM Clock")

    width = 1280
    height = 800
    screen = pygame.display.set_mode( (width, height) )

    pygame.freetype.init()
    font = pygame.freetype.SysFont( pygame.freetype.get_default_font(), 16, True, False)

    #surface = pygame.Surface( (width, height) )
    rect = pygame.Rect(0, 0, width, height)
    black = (0, 0, 0)
    red = (255, 0, 0)

    minute_clock = pygame.sprite.Group()
    square_len = int( min(width, height) * 0.8 )
    tach_rect = pygame.Rect(0, 0, square_len, square_len)
    tach_rect.center = (width//2, height//2)

    #minute_clock.add(tach_arc)

    hour_clock = pygame.sprite.Group()

    '''
    all_group = pygame.sprite.Group()
    all_group.add(hour_clock)
    all_group.add(minute_clock)
    '''

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill( black )

        #time = datetime.now()

        ## draw clock
        pygame.draw.arc(screen, red, tach_rect, 2*math.pi*0.85, 2*math.pi*0.65, 15)
        pygame.draw.aaline(screen, red, (0, 0), (width, height), 20)

        font.origin = True
        font.render_to(screen, (width//2, height//2), "THIS IS A TEST", red, size = 20)

        for i in range(5, 65, 5):
            #pygame.
            pass

        pygame.display.update()

    pygame.freetype.quit()

if __name__ == "__main__":
    main()

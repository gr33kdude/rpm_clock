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
    pygame.display.set_caption("RPM Clock")

    width = 1280
    height = 800
    screen = pygame.display.set_mode( (width, height) )

    pygame.freetype.init()
    font = pygame.freetype.SysFont( pygame.freetype.get_default_font(), 16, True, False)

    pygame.key.set_repeat(80)

    black = (0, 0, 0)
    red = (255, 0, 0)

    minute_clock = pygame.sprite.Group()
    square_len = int( min(width, height) * 0.6 )
    speed_rect = pygame.Rect(0, 0, square_len, square_len)
    speed_rect.center = (width//2, height//2)

    #minute_clock.add(tach_arc)

    hour_clock = pygame.sprite.Group()

    '''
    all_group = pygame.sprite.Group()
    all_group.add(hour_clock)
    all_group.add(minute_clock)
    '''

    min_speed = 0
    max_speed = 60
    speed_len = max_speed - min_speed
    speed = 0

    # map 0 to 60 to 65% of the circle to 85% of the circle
    start_pct = 0.65
    end_pct   = 0.85

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    speed -= 1
                elif event.key == pygame.K_UP:
                    speed += 1
        
        # cap/bound speed
        speed = max(min(speed, max_speed), min_speed)

        screen.fill( black )

        ## draw clock
        pygame.draw.arc(screen, red, speed_rect,
                2*math.pi * end_pct, 2*math.pi*start_pct, 3)
        #pygame.draw.line(screen, red, (0, 0), (width, height), 20)

        s = str(speed)
        #font.render_to(screen, (width//2, height//2), s, red, size = 20)
        font.origin = True
        text, rect = font.render(s, red, size=24)
        rect = text.get_rect(center = (width//2, height//2))
        rect.top += 50
        screen.blit(text, rect)

        # draw needle
        radius = square_len/2
        angle_len = start_pct + (1 - end_pct)

        angle = (speed / speed_len) * angle_len
        angle = ((start_pct - angle) * 2*math.pi)
        theta = angle
        
        L = 14
        for i in range(L):
            r = 0.7 * radius * (L-i) / L
            center_x, center_y = speed_rect.centerx, speed_rect.centery
            end_x = center_x + r * math.cos(theta)
            end_y = center_y - r * math.sin(theta)
            pygame.draw.line(screen, red, (center_x, center_y), (end_x, end_y), i+1)

        # draw tachometer
        d = 1.3 * radius
        a = math.acos(d / 2 / radius)

        tach_rect = speed_rect.move( (-d, 0) )
        pygame.draw.arc(screen, red, tach_rect, a, 2*math.pi*start_pct, 3)

        L = 14
        for i in range(L):
            r = 0.7 * radius * (L-i) / L
            center_x, center_y = tach_rect.centerx, tach_rect.centery
            end_x = center_x + r * math.cos(theta)
            end_y = center_y - r * math.sin(theta)
            pygame.draw.line(screen, red, (center_x, center_y), (end_x, end_y), i+1)

        pygame.display.update()

    pygame.freetype.quit()

if __name__ == "__main__":
    main()

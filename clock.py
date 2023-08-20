#!/usr/bin/env python3

import pygame
import pygame.freetype
from datetime import datetime
import math

# need to know what time it is

# show the display
# tachometer on the left side for RPM / hour
# big speedometer in the center
# fuel gauge shows the battery percentage

# find a way to draw the clock
# draw each subcomponent
# done

def display_speed(screen, color, rect, s, font):
    font.origin = True
    text, text_rect = font.render(s, color, size=74)
    text_rect = text.get_rect(center = (rect.centerx, rect.centery))
    text_rect.top += rect.height * 0.34
    screen.blit(text, text_rect)

def draw_needle(screen, color, rect, radius, theta):
    N = 20
    for i in range(N):
        r = 0.7 * radius * math.pow((N-i) / N, 1.3)

        cx, cy = rect.centerx, rect.centery
        end_x = cx + r * math.cos(theta)
        end_y = cy - r * math.sin(theta)

        pygame.draw.line(screen, color, (cx, cy), (end_x, end_y), i+1)

def draw_tach():
    pass

def draw_arc_text(screen, color, rect, font, input_len, input_start, increment, output_len, output_start):
    input_end = input_start + input_len
    for i in range(input_start, input_end, increment):
        font.origin = True
        text, text_rect = font.render( str(i), color, size = 24 )

        angle = ((i - input_start) / input_len) * output_len
        angle = ((output_start - angle) * 2*math.pi)
        theta = angle

        r = 0.82 * min(rect.width, rect.height) / 2
        point = lambda r, theta: \
            ( rect.centerx + r * math.cos(theta), rect.centery - r * math.sin(theta) )
        text_rect = text.get_rect(center = point(r, theta))
        screen.blit(text, text_rect)

def draw_arc_lines(screen, color, rect, input_len, output_len, output_start, width = 3):
    radius = min(rect.width, rect.height) / 2

    for i in range(0, input_len+1):
        angle = (i / input_len) * output_len
        angle = ((output_start - angle) * 2*math.pi)
        theta = angle

        point = lambda r, theta: \
            ( rect.centerx + r * math.cos(theta), rect.centery - r * math.sin(theta) )
        start = point( 0.92 * radius, theta)
        end   = point( 1.00 * radius, theta)

        pygame.draw.line(screen, color, (start[0], start[1]), (end[0], end[1]), width)

def draw_speedo():
    pass

def main():
    pygame.init()
    pygame.display.set_caption("RPM Clock")

    width = 1280
    height = 800
    screen = pygame.display.set_mode( (width, height) )

    pygame.freetype.init()
    font = pygame.freetype.SysFont( pygame.freetype.get_default_font(), 16, True, False)

    pygame.key.set_repeat(95)

    black   = (0, 0, 0)
    red     = (255, 0, 0)
    green   = (0, 215, 0)
    d_green = (0, 195, 0)
    l_blue  = (102, 178, 255)
    blue    = (0, 0, 255)
    pink    = (255, 51, 255)
    l_pink  = (255, 151, 255)
    orange  = (255, 128, 0)
    gray    = (240, 240, 240)
    white   = (255, 255, 255)

    square_len = int( min(width, height) * 0.6 )
    gauge_radius = square_len/2
    speed_rect = pygame.Rect(0, 0, square_len, square_len)

    gauge_offset = 1.3
    gauge_width = gauge_offset * gauge_radius

    left = width - ((width - gauge_width)/2)
    speed_rect.center = (left, height//2)

    min_speed = 0
    max_speed = 59
    speed_len = max_speed - min_speed + 1
    speed = min_speed
    speed_pctg = lambda speed: (speed - min_speed) / speed_len

    min_display_tach = 0
    min_tach         = 1
    max_display_tach = 12
    max_tach         = max_display_tach

    tach_display_len = max_display_tach - min_display_tach + 1
    tach_len = max_tach - min_tach + 1
    tach = min_tach
    tach_pctg = lambda tach: (tach - min_display_tach) / tach_display_len

    time_mode = True
    time_mode_numb = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    speed -= 1
                elif event.key == pygame.K_k:
                    speed += 1
                elif event.key == pygame.K_d:
                    tach -= 1
                elif event.key == pygame.K_f:
                    tach += 1
                elif event.key == pygame.K_t and not time_mode_numb:
                    time_mode = not time_mode
                    time_mode_numb = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_t:
                    if time_mode_numb:
                        time_mode_numb = False

        if time_mode:
            now = datetime.now()
            tach = (now.hour % 12)
            if tach % 12 == 0:
                tach = 12

            speed = now.minute
        
        cap = lambda x, Min, Max: max(min(x, Max), Min)
        # cap/bound speed
        speed = cap(speed, min_speed, max_speed)
        # cap/bound tach
        tach  = cap(tach, min_tach, max_tach)

        screen.fill( black )

        speed_radius = min(speed_rect.width, speed_rect.height) / 2
        radius = speed_radius

        # draw tachometer
        tach_radius = speed_radius
        d = gauge_offset * tach_radius
        arc_intercept = math.acos(d / 2 / tach_radius)
        tach_rect = speed_rect.move( (-d, 0) )

        tach_start = 0.65
        tach_end   = arc_intercept / (2*math.pi)

        tach_angle_len = tach_start - tach_end
        angle = tach_pctg(tach) * tach_angle_len
        angle = (tach_start - angle) * 2*math.pi
        theta = angle

        pygame.draw.circle(screen, gray, tach_rect.center, tach_radius)
        pygame.draw.arc(screen, orange, tach_rect, arc_intercept, 2*math.pi*tach_start, 8)

        draw_arc_text(screen, black, tach_rect, font, tach_display_len, 0, 1, tach_angle_len, tach_start)
        draw_arc_lines(screen, blue, tach_rect, tach_display_len, tach_angle_len, tach_start, 6)

        draw_needle(screen, red, tach_rect, tach_radius, theta)
        tach_color = d_green if time_mode else pink
        display_speed(screen, tach_color, tach_rect, str(tach), font)

        ## draw clock
        # map 0 to 60 mph to 65% of the circle to 85% of the circle
        speed_start = 0.65
        speed_end   = 0.85

        speed_angle_len = speed_start + (1 - speed_end)
        angle = speed_pctg(speed) * speed_angle_len
        angle = (speed_start - angle) * 2*math.pi
        theta = angle

        pygame.draw.circle(screen, white, speed_rect.center, speed_radius)
        pygame.draw.arc(screen, orange, speed_rect, 2*math.pi * speed_end, 2*math.pi * speed_start, 10)

        draw_arc_text(screen, black, speed_rect, font, speed_len, 0, 5, speed_angle_len, speed_start)
        draw_arc_lines(screen, blue, speed_rect, speed_len, speed_angle_len, speed_start)

        draw_needle(screen, red, speed_rect, speed_radius, theta)
        speed_color = green if time_mode else l_pink
        display_speed(screen, speed_color, speed_rect, str(speed), font)

        # closing things
        pygame.display.update()
        pygame.time.wait(10)

    pygame.freetype.quit()

if __name__ == "__main__":
    main()

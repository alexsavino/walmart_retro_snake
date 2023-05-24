import pygame as pyg
from pygame.locals import *
import numpy as np
'''
import sys
sys.stdout = open('output.log', 'w')
'''

# INITIALIZING THE GENERAL SCREEN...
pyg.init()
width, height = 640, 480
screen = pyg.display.set_mode((width,height))
title_font = pyg.font.Font(None,80)
subtitle_font = pyg.font.Font(None,30)



# INITIALIZING SCREENS...
title_screen = True
option_screen = False
game_screen = False
final_screen = False
PREVIOUS_PAGE = title_screen
TEST_SCREEN = True 


# CREATING SCREEN CONDITIONS...
# PRIMARY GAME LOOP...
while True:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    while title_screen:
        pyg.display.set_caption("Snake Game")
        screen.fill('black')

        title = title_font.render("SNAKE GAME", True, 'white')
        subtitle = subtitle_font.render("PRESS 'SPACE' TO START", True, 'white')
        title_rect = title.get_rect(center=(width//2, height//2-20))
        subtitle_rect = subtitle.get_rect(center=(width//2, height//2 + 25))

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        for event in pyg.event.get():
            if (event.type==KEYDOWN) and (event.key==K_SPACE):
                title_screen = False
                option_screen = True

        pyg.display.flip()


    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    gen_col = 'white'  # gen_option_sc_txt_color

    def back_arrow():
        global vertices
        arrow_color = 'red'
        x = 3
        y = 5
        dilation = 5
        back_arrow_vertices = list(dilation * np.array([(x, y), (x + 3, y + 2.5), (x + 3, y + 1.25), 
                    (x + 7, y + 1.25), (x + 7, y - 1.25), (x + 3, y - 1.25), (x + 3, y - 2.5)]))
        vertices = pyg.draw.polygon(screen, arrow_color, back_arrow_vertices, width=2)
        return back_arrow_vertices

    def is_inside_arrow(point,arrow_vertices):
        x, y = point
        n = len(arrow_vertices)
        inside = False
        p1x, p1y = arrow_vertices[0]
        for i in range(n + 1):
            p2x, p2y = arrow_vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_intersect:
                                inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    cursor_visible = True
    cursor_timer, cursor_interval = 0, 600

    q_font = pyg.font.Font(None, 25)
    a_font = pyg.font.Font(None, 22)
    name_question = "1. WHAT'S YOUR NAME?: "
    username = ""

    while option_screen:
        screen.fill('black')
        pyg.display.set_caption("___'s Game Settings")

        # TO CREATE BACK-BUTTON!
        back_arrow_polygon = back_arrow()

        # TO RECORD THE USER'S NAME... 
        for event in pyg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    username = username[:-1]
                elif event.key == K_RETURN:
                    username = username.rstrip()
                    pyg.display.set_caption("{}'s Game Settings".format(username))
                elif event.unicode.isalpha() or event.unicode.isspace():
                    username += event.unicode
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                mouse_pos = pyg.mouse.get_pos()
                if is_inside_arrow(mouse_pos, back_arrow_polygon):
                    # HERE HERE HERE HERE HERE 
                    title_screen = True
                    option_screen = False
                    break


        # TO POSITION BOTH QUESTION / ANSWER...
        q_top, q_left = 75, 75
        q_surface = q_font.render(name_question, True, gen_col)
        q_rect = q_surface.get_rect(topleft=(q_left, q_top))
        screen.blit(q_surface, q_rect)

        a_top, a_left = (q_top+1.5), q_rect.right + 3
        a_surface = a_font.render(username, True, gen_col)
        a_rect = a_surface.get_rect(topleft=(a_left, a_top))
        screen.blit(a_surface, a_rect)

        # TO MAKE THE CURSOR BLINK...
        cursor_timer += 1
        if cursor_timer >= cursor_interval:
            cursor_timer = 0
            cursor_visible = not cursor_visible

        if cursor_visible:
            cursor_x = a_rect.right + 2  # Adjust the cursor x position
            cursor_surface = a_font.render("_", True, gen_col)
            cursor_rect = cursor_surface.get_rect(topleft=(cursor_x, a_top))
            screen.blit(cursor_surface, cursor_rect)

        pyg.display.flip()

# maybe i can make it so that when you do hit enter on your name quotes appear? maybe a color change? something to differentiate



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#while game_screen():
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#while end_screen():

pyg.quit()

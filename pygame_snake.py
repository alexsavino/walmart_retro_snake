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
gen_col = 'white'  # gen_option_sc_txt_color


# INITIALIZING SCREENS...
title_screen = True
option_screen = False
game_screen = False
final_screen = False
#PREVIOUS_PAGE = title_screen # is this format / connection builder im rly gonna use?



# FUNCTIONS THAT RELATE THE SCREENS...
def back_arrow():
    arrow_color = 'red'

    # TO DRAW THE NEUTRAL ARROW OUTLINE...
    x = 3
    y = 5
    dilation = 5
    back_arrow_vertices = list(dilation * np.array([(x, y), (x+3, y+2.5), (x+3, y+1.25), 
                (x+7, y+1.25), (x+7, y-1.25), (x+3, y-1.25), (x+3, y-2.5)]))
    pyg.draw.polygon(screen, arrow_color, back_arrow_vertices, width=2)

    # TO ENABLE HOVER COLOR...
    if is_inside_arrow(mouse_pos, back_arrow_vertices):
        polygon_surface = pyg.Surface((width,height), pyg.SRCALPHA)
        pyg.draw.polygon(polygon_surface, arrow_color, back_arrow_vertices)
        screen.blit(polygon_surface, (0, 0))
     
    return back_arrow_vertices


def forward_arrow():
    arrow_color = 'green'

    # TO DRAW THE NEUTRAL ARROW OUTLINE...
    x = 124.5
    y = 90
    dilation = 5
    forward_arrow_vertices = list(dilation * np.array([(x, y), (x-3, y+2.5), (x-3, y+1.25), 
                (x-7, y+1.25), (x-7, y-1.25), (x-3, y-1.25), (x-3, y-2.5)]))
    pyg.draw.polygon(screen, arrow_color, forward_arrow_vertices, width=2)

    # TO ENABLE HOVER COLOR...
    if is_inside_arrow(mouse_pos, forward_arrow_vertices):
        polygon_surface = pyg.Surface((width,height), pyg.SRCALPHA)
        pyg.draw.polygon(polygon_surface, arrow_color, forward_arrow_vertices)
        screen.blit(polygon_surface, (0, 0))

    return forward_arrow_vertices


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

hovered_color = None
# CREATING SCREEN CONDITIONS...
# PRIMARY GAME LOOP...
while True:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    SPACE_timer = 0

    while title_screen:
        pyg.display.set_caption("Snake Game")
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()

        title_font = pyg.font.Font(None,80)
        subtitle_font = pyg.font.Font(None,30)
        SPACE_font = pyg.font.Font(None,35)

        # TO MAKE THE TITLE + SUBTITLE...
        title_title = title_font.render("SNAKE GAME", True, gen_col)
        subtitle = subtitle_font.render("PRESS                TO START", True, gen_col)
        title_height = height//2-20
        subtitle_height = height//2 + 25
        title_rect = title_title.get_rect(center=(width//2, title_height))
        subtitle_rect = subtitle.get_rect(center=(width//2, subtitle_height))

        screen.blit(title_title, title_rect)
        screen.blit(subtitle, subtitle_rect)


        # TO MAKE THE 'SPACE' BLINK...
        SPACE_visible = True
        SPACE_timer += 1
        time_not_visible = 700
        time_visible = 2000
        if SPACE_timer < time_not_visible:
            SPACE_visible = not SPACE_visible
        elif SPACE_timer >= time_visible:
            SPACE_timer = 0
    
        if SPACE_visible:
            SPACE_x = width//2-54
            SPACE_surface = SPACE_font.render("SPACE", True, gen_col)
            SPACE_rect = SPACE_surface.get_rect(topleft=(SPACE_x, subtitle_height-13))
            screen.blit(SPACE_surface, SPACE_rect)


        # EVENTS CAPTURE...
        for event in pyg.event.get():
            if (event.type == pyg.QUIT):
                pyg.quit()
            elif (event.type==KEYDOWN) and (event.key==K_SPACE):
                title_screen = False
                option_screen = True

        pyg.display.flip()


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    cursor_visible = True
    cursor_timer, cursor_interval = 0, 600

    q_font = pyg.font.Font(None, 25)
    a_font = pyg.font.Font(None, 22)

    # LIST OF OPTION QUESTIONS...
    name_question = "1. WHAT'S YOUR NAME?: "
    username = ""
    snake_color_question = "2. SNAKE COLOR?: "
    pellet_color_question = "3. PELLET COLOR?: "
    board_color_question = "4. BOARD COLOR?: "

    while option_screen:
        screen.fill('black')
        pyg.display.set_caption("Game Settings")
        mouse_pos = pyg.mouse.get_pos()

        # TO CREATE BACK-BUTTON!
        back_arrow_polygon_option = back_arrow()
        forward_arrow_polygon_option = forward_arrow()

        # SCREEN TITLE...
        option_title_font = pyg.font.Font(None,50)
        option_title = option_title_font.render("GAME SETTINGS", True, gen_col)
        option_title_height = 46
        option_title_rect = option_title.get_rect(center=(width//2,option_title_height))
        screen.blit(option_title, option_title_rect)

        space_between_questions = 88
        
        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 1: NAME


        # TO POSITION BOTH QUESTION / ANSWER...
        q_left, q_top = 75, 100
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


        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 2: SNAKE COLOR
        snake_q_left, snake_q_top = q_left, (q_top+space_between_questions)
        snake_q_surface = q_font.render(snake_color_question, True, gen_col)
        snake_q_rect = snake_q_surface.get_rect(topleft=(snake_q_left,snake_q_top))
        screen.blit(snake_q_surface,snake_q_rect)



        def color_bar_caption(snake_color):
            snake_color_width = 360
            snake_color_height_adj = 33
            snake_color_height = snake_q_top + snake_color_height_adj
            snake_color_rect = snake_color.get_rect(center=(snake_color_width,snake_color_height))
            screen.blit(snake_color, snake_color_rect)
        
        def color_bar_system():

            global hovered_color

            color_options = ['RED','ORANGE','YELLOW','GREEN','BLUE','PURPLE']

            for color_index in range(len(color_options)):
                # DRAWING THE COLORED RECTANGLES...
                color_box_width = 30
                color_box_x = snake_q_rect.right + 30 + (color_index * color_box_width)
                color_box_height_adj = -17
                color_box_y = snake_q_top + color_box_height_adj
                given_box = pyg.Rect(color_box_x,color_box_y,
                    color_box_width,color_box_width)
                pyg.draw.rect(screen, color_options[color_index], given_box)
                
                # TO SEE IF THE MOUSE IS HOVERING OVER EACH BOX...
                if given_box.collidepoint(mouse_pos):
                    snake_color = a_font.render(str(color_options[color_index]), 
                        True, gen_col)
                    color_bar_caption(snake_color)
                    hovered_color = color_options[color_index]

            if hovered_color:
                snake_color = a_font.render(str(hovered_color), True, gen_col)
                color_bar_caption(snake_color)

                #pyg.draw.rect(screen, gen_col, given_box, width=2)
 
        color_bar_system()



        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 4: PELLET COLOR
        pellet_q_left, pellet_q_top = q_left, (snake_q_top+space_between_questions)
        pellet_q_surface = q_font.render(pellet_color_question, True, gen_col)
        pellet_q_rect = pellet_q_surface.get_rect(topleft=(pellet_q_left,pellet_q_top))
        screen.blit(pellet_q_surface,pellet_q_rect)

        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 3: BOARD COLOR
        board_q_left, board_q_top = q_left, (pellet_q_top+space_between_questions)
        board_q_surface = q_font.render(board_color_question, True, gen_col)
        board_q_rect = board_q_surface.get_rect(topleft=(board_q_left,board_q_top))
        screen.blit(board_q_surface,board_q_rect)





        # EVENTS CATCHER...
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
            # TO ENTER USERNAME...
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    username = username[:-1]
                # THIS COULD USE SOME CLEANING UP!!
                elif event.key == K_RETURN:
                    username = username.rstrip()
                    pyg.display.set_caption("{}'s Game Settings".format(username))
                # THIS COULD USE SOME CLEANING UP!!
                # 1. can't let users enter tabs -- results in something weird
                # 2. should be a reasonable length check
                # 3. ...
                elif event.unicode.isalpha() or event.unicode.isspace():
                    if event.unicode != '\t':
                        username += event.unicode
            # WHAT HAPPENS WHEN THE MOUSE IS CLICKED...
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
                if is_inside_arrow(mouse_pos, back_arrow_polygon_option):
                    title_screen = True
                    option_screen = False
                    break
                # WHAT HAPPENS IF FORWARD BUTTON IS PRESSED...
                if is_inside_arrow(mouse_pos, forward_arrow_polygon_option):
                    game_screen = True
                    option_screen = False
                    break
            # WHAT HAPPENS WHEN YOU CLICK ON THE COLOR BOXES?
            # ... 

        pyg.display.flip()


# maybe i can make it so that when you do hit enter on your name quotes appear? 
#   maybe a color change? put a white box around it? something to differentiate
#   how could you go back and edit it yourself?


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    while game_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()

        # TEST_USERNAME // TEST_USERNAME // TEST_USERNAME // TEST_USERNAME
        TEST_USERNAME = 'Alex'
        pyg.display.set_caption("{}'s Snake Game".format(TEST_USERNAME))


        # EVENTS CATCHER...
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
            # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
            # ...
            
        pyg.display.flip()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # this is what should be presented SHOULD A GAME BE FINISHED!
    # 1. the results - 'YOU LOST', 'YOU WON'
    # 2. 'play again!!'
    # 3. (settings?)
    '''
    while end_screen():
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        pyg.display.set_caption("RESULTS PAGE")

        # EVENTS CATCHER...
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()

        pyg.display.flip()
    '''

pyg.quit()

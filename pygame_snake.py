#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# -*- coding: utf-8 -*-
# @Date:    2023-05-23 12:07:44
# @Author:  ALEXANDRA SAVINO 
# @Email:   avs2167@barnard.edu

# Legend:
#   '# ?? ___' = something to be revisited, a question
#   '# !! ___' = an exciting note!, new idea
#   '# PLACEHOLDER' = a placeholding value of some kind

import pygame as pyg
from pygame.locals import *
import numpy as np
import random as rand
import sys
'''
import sys
sys.stdout = open('output.log', 'w')
'''

# INITIALIZING THE GENERAL SCREEN...
pyg.init()
width, height = 640, 480
screen = pyg.display.set_mode((width,height))
gen_col = 'white'  # gen_option_sc_txt_color
clock = pyg.time.Clock()

# INITIALIZING SCREENS...
title_screen = False
option_screen = False
game_screen = False
end_screen = True

# TO CREATE MAC DISPLAY NAME IN THE CASE OF NO USERNAME...
animal_list = ['Fox','Robin','Chipmunk','Squirrel','Deer']
round_animal_name = rand.choice(animal_list)
    
# INSTANTIATING THE ARRAY SQUARE PROPERTIES...
square_size = 18
row_span = (width-75)
col_span = (height-100)
num_rows = col_span // square_size
num_cols = row_span // square_size

# TO POSITION THE ARRAY...
board_x = (width - (num_cols * square_size)) / 2
board_y = 78


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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


def color_bar_caption(color, q_top):
    color_width = 360
    color_height_adj = 33
    color_height = q_top + color_height_adj
    color_rect = color.get_rect(center=(color_width, color_height))
    screen.blit(color, color_rect)


color_options = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE']
def color_bar_system(q_rect, q_top, line_identifier):
    global hovered_colors
    global snake_color, pellet_color, board_color
    global color_options

    for color_index in range(len(color_options)):
        # DRAWING THE COLORED RECTANGLES...
        color_box_width = 30
        color_box_x = q_rect.right + 30 + (color_index * color_box_width)
        color_box_height_adj = -17
        color_box_y = q_top + color_box_height_adj
        given_box = pyg.Rect(color_box_x, color_box_y, color_box_width, color_box_width)
        pyg.draw.rect(screen, color_options[color_index], given_box)
        
        # TO SEE IF THE MOUSE IS HOVERING OVER EACH BOX...
        if given_box.collidepoint(mouse_pos):
            color = a_font.render(str(color_options[color_index]), True, gen_col)
            color_bar_caption(color, q_top)
            hovered_colors[line_identifier] = color_options[color_index]

            # Draw rectangle around the hovered box
            pyg.draw.rect(screen, gen_col, given_box, width=2)

    if line_identifier in hovered_colors:
        color = a_font.render(str(hovered_colors[line_identifier]), True, gen_col)
        color_bar_caption(color, q_top)

        # Draw rectangle around the last hovered box
        last_hovered_box_index = color_options.index(hovered_colors[line_identifier])
        last_hovered_box_x = q_rect.right + 30 + (last_hovered_box_index * color_box_width)
        last_hovered_box_y = q_top + color_box_height_adj
        last_hovered_box = pyg.Rect(last_hovered_box_x, last_hovered_box_y, color_box_width, color_box_width)
        pyg.draw.rect(screen, gen_col, last_hovered_box, width=2)

        if line_identifier == 'snake':
            snake_color = hovered_colors[line_identifier]
            return snake_color
        elif line_identifier == 'pellet':
            pellet_color = hovered_colors[line_identifier]
            return pellet_color
        elif line_identifier == 'board':
            board_color = hovered_colors[line_identifier]
            return board_color

hovered_colors = {}


def draw_array(board_color_1,board_color_2):
    for row in range(num_rows):
        for col in range(num_cols):
            x = board_x + col * square_size
            y = board_y + row * square_size
            color = board_color_1 if (row + col) % 2 == 0 else board_color_2
            pyg.draw.rect(screen, color, (x, y, square_size, square_size))


def clear_array():
    x = board_x
    y = board_y
    width = num_cols * square_size
    height = num_rows * square_size
    pyg.draw.rect(screen, 'black', (x, y, width, height))
    draw_border_lines()


# TO MAKE THE ARRAY BLINK...
def blink_array(self_collision=False):
    global game_screen, end_screen
    num_of_blinks = 3
    blink_interval = 0.3
    # ?? snake_head = snake_segments[0] ??

    clear_snake(snake_segments)
    if (self_collision == True):
        pyg.time.wait(int(blink_interval * 5000)) 
    for _ in range(num_of_blinks):
        clear_array()
        pyg.display.flip()
        pyg.time.wait(int(blink_interval * 1000)) 

        draw_array(board_color_1, board_color_2)
        pyg.display.flip()
        pyg.time.wait(int(blink_interval * 1000))

    # TO CHANGE SCREENS...
    pyg.time.wait(int(blink_interval * 5000)) 
    game_screen = False
    end_screen = True


def draw_snake(snake_segments):
    for segment in snake_segments:
        x, y = segment
        pyg.draw.rect(screen, snake_color, (x, y, square_size, snake_width))


def clear_snake(snake_segments):
    for segment in snake_segments:
        x, y = segment
        pyg.draw.rect(screen, 'black', (x, y, square_size, snake_width))

'''
#def add_snake_segment(snake_segments):
    # this has to look at the last few blocks, determine which block is the last block and its direction
    #   based on the block in front of it... then it has to actually add the new block and update 'snake_segments'
'''



pellet_x = 0
pellet_y = 0
def get_pellet_rect():
    global pellet_x, pellet_y, square_size
    pellet_rect = pyg.Rect(pellet_x, pellet_y, square_size, square_size)
    return pellet_rect


def draw_pellet(pellet_color):
    global pellet_x, pellet_y, board_x, board_y, pellet_rect

    if pellet_x == 0 and pellet_y == 0:
        pellet_x = board_x + (rand.randint(1, num_cols - 1) * square_size)
        pellet_y = board_y + (rand.randint(1, num_rows - 1) * square_size)

    pellet_rect = get_pellet_rect()

    # TO DRAW A BLACK BORDER AROUND THE PELLET...
    pyg.draw.line(screen, 'black', (pellet_x, pellet_y), (pellet_x + square_size, pellet_y), width=1)
    pyg.draw.line(screen, 'black', (pellet_x + square_size, pellet_y), (pellet_x + square_size, pellet_y + square_size), width=1)
    pyg.draw.line(screen, 'black', (pellet_x + square_size, pellet_y + square_size), (pellet_x, pellet_y + square_size), width=1)
    pyg.draw.line(screen, 'black', (pellet_x, pellet_y + square_size), (pellet_x, pellet_y), width=1)

    pyg.draw.rect(screen, pellet_color, pellet_rect)


    # !! IF YOU COLLIDE YOU LOSE 5 PELLETS & IF YOU REACH 0 YOU AUTOMATICALLY LOSE !!

pellet_counter = 0
pellet_counter_history = []
print(type(pellet_counter))

def pellet_tracker(snake_segments):
    global pellet_counter
    x, y = snake_segments[0]
    snake_head_rect = pyg.Rect(x, y, square_size, square_size)

    if snake_head_rect.colliderect(get_pellet_rect()):
        #print('*PELLET collision')
        pellet_counter += 1
        
        # ?? CLEAR PELLET ??
        # ?? PRINT NEW PELLET ??
        # ?? ADD A NEW SNAKE SEGMENT ONTO THE END ??






def draw_border_lines():
    global line_1, line_2, line_3, line_4

    # Top line...
    line_1 = (board_x, board_y - 1, width - board_x, board_y - 1)
    # Left line...
    line_2 = (board_x - 1, board_y, board_x - 1, board_y + col_span - 3)
    # Right line...
    line_3 = (width - board_x + 1, board_y, width - board_x + 1, board_y + col_span - 3)
    # Bottom line...
    line_4 = (board_x, board_y + col_span - 2, width - board_x, board_y + col_span - 2)

    pyg.draw.line(screen, gen_col, line_1[0:2], line_1[2:4], width=1)
    pyg.draw.line(screen, gen_col, line_2[0:2], line_2[2:4], width=1)
    pyg.draw.line(screen, gen_col, line_3[0:2], line_3[2:4], width=1)
    pyg.draw.line(screen, gen_col, line_4[0:2], line_4[2:4], width=1)


def check_snake_collision(snake_segments):
    global game_screen, end_screen
    x, y = snake_segments[0]
    snake_head_rect = pyg.Rect(x, y, square_size, square_size)

    if snake_head_rect.clipline(line_1[0:2], line_1[2:4]) or \
       snake_head_rect.clipline(line_2[0:2], line_2[2:4]) or \
       snake_head_rect.clipline(line_3[0:2], line_3[2:4]) or \
       snake_head_rect.clipline(line_4[0:2], line_4[2:4]):
        clock.tick(1)
        blink_array()

    for segment in snake_segments[1:]:
        x, y = segment[0], segment[1]
        segment_rect = pyg.Rect(x, y, square_size, square_size)
        if snake_head_rect.colliderect(segment_rect):
            blink_array(self_collision=True)
    
    # !! IF YOU COLLIDE ***WITH YOURSELF*** YOU LOSE 5 PELLETS & IF YOU REACH 0 YOU AUTOMATICALLY LOSE !!




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# PRIMARY GAME LOOP...
while True:

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
        time_not_visible = 825
        time_visible = 700

        if (SPACE_timer > time_visible) and (SPACE_timer < time_not_visible):
            SPACE_visible = not SPACE_visible
        elif SPACE_timer >= time_not_visible:
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

        # TO CREATE SCREEN-BUTTONS!
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
        color_bar_system(snake_q_rect,snake_q_top,'snake')

        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 4: PELLET COLOR
        pellet_q_left, pellet_q_top = q_left, (snake_q_top+space_between_questions)
        pellet_q_surface = q_font.render(pellet_color_question, True, gen_col)
        pellet_q_rect = pellet_q_surface.get_rect(topleft=(pellet_q_left,pellet_q_top))
        screen.blit(pellet_q_surface,pellet_q_rect)
        color_bar_system(pellet_q_rect,pellet_q_top,'pellet')

        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 3: BOARD COLOR
        board_q_left, board_q_top = q_left, (pellet_q_top+space_between_questions)
        board_q_surface = q_font.render(board_color_question, True, gen_col)
        board_q_rect = board_q_surface.get_rect(topleft=(board_q_left,board_q_top))
        screen.blit(board_q_surface,board_q_rect)
        color_bar_system(board_q_rect,board_q_top,'board')


        # EVENTS CATCHER...
        for event in pyg.event.get():
            if (event.type == pyg.QUIT):
                pyg.quit()
            # TO ENTER USERNAME...
            elif event.type == KEYDOWN:
                if (event.key == K_BACKSPACE):
                    username = username[:-1]

                elif event.unicode.isalpha() or event.unicode.isspace():
                    if (event.unicode != '\t') and (event.key != 13) and (len(username) < 20):
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

        pyg.display.flip()

    username = username.strip()

# ?? HOW TO MAKE IT SO THAT SOMEONE'S NAME STAYS EVEN AS YOU 
#    GO BACK AND FORTH BETWEEN OPTION AND GAME SCREENS??
# ?? maybe i can make it so that when you do hit enter on your name quotes appear? 
#   maybe a color change? put a white box around it? something to differentiate
#   how could you go back and edit it yourself?


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # TO CREATE MAC DISPLAY NAME IN THE CASE OF NO USERNAME...
    anonymous_username = pyg.display.set_caption("Anonymous {}'s Snake Game".format(round_animal_name))
                                                 
    TEST_BOARD_COLOR = 'PURPLE' # PLACEHOLDER ... supposed to be 'board_color'
    snake_color = 'BLUE' # TEST_SNAKE_COLOR
    pellet_color = 'RED' #TEST_PELLET_COLOR

    # TO INSTANTIATE THE SNAKE...
    snake_box_length = 3   # ?? IS THIS SOMETHING TO PULL OUT OF THIS WHILE LOOP?
    snake_length = snake_box_length * square_size
    snake_width = square_size

    snake_x = board_x + (10 * square_size)
    snake_y = board_y + (10 * square_size)
    snake_direction = 'right'
    snake_segments = []

    for square in range(snake_box_length):
        segment_x = snake_x - (snake_box_length - square) * square_size
        segment_y = snake_y
        snake_segments.append((segment_x, segment_y))

    snake_segments = snake_segments[::-1]

    # TO DETERMINE BOTH BOARD COLORS...
    board_colors = [['red','tomato'],['chocolate','orange'],['gold','yellow'],
        ['green','limegreen'],['blue','royalblue'],['darkviolet','mediumorchid']]
    
    board_color_1 = board_colors[color_options.index(TEST_BOARD_COLOR)][0]
    board_color_2 = board_colors[color_options.index(TEST_BOARD_COLOR)][1]
    
    
    while game_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        clock.tick(10)

        #$$$$
        pellet_tracker(snake_segments)


        # TO CREATE MAC DISPLAY NAME...
        if username == "":
            anonymous_username
        else:
            pyg.display.set_caption("{}'s Snake Game".format(username))

        # TO CREATE SCREEN-BUTTONS!
        back_arrow_polygon_option = back_arrow()
        # ?? the options will be to either 1. quit the game and go to the option screen ....

        # SCREEN TITLE...
        game_title_font = pyg.font.Font(None,50)
        game_title = game_title_font.render("!~SNAKE GAME~!", True, gen_col)
        game_title_height = 46
        game_title_rect = game_title.get_rect(center=(width//2,game_title_height))
        screen.blit(game_title, game_title_rect)


        # TO DRAW THE ARRAY... 
        draw_array(board_color_1,board_color_2)

        
        # TO DRAW THE SNAKE...
        snake_segments.pop()

        # EVENTS CATCHER...
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
            # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                if is_inside_arrow(mouse_pos, back_arrow_polygon_option):
                # 1. 'are you sure you wanna quit the game?' y/n
                #   (and it PAUSES YOUR GAME)
                # 2. 
                    option_screen = True
                    game_screen = False
                    break
            
            elif event.type == KEYDOWN:
                if event.key == pyg.K_UP and snake_direction != 'down':
                    snake_direction = 'up'
                elif event.key == pyg.K_DOWN and snake_direction != 'up':
                    snake_direction = 'down'
                elif event.key == pyg.K_LEFT and snake_direction != 'right':
                    snake_direction = 'left'
                elif event.key == pyg.K_RIGHT and snake_direction != 'left':
                    snake_direction = 'right'

        # TO CALCULATE NEW HEAD SQUARE + SHIFT UP OTHER SQUARES...
        if snake_direction == 'up':
            new_segment_x = snake_segments[0][0]
            new_segment_y = snake_segments[0][1] - square_size
        elif snake_direction == 'down':
            new_segment_x = snake_segments[0][0]
            new_segment_y = snake_segments[0][1] + square_size
        elif snake_direction == 'left':
            new_segment_x = snake_segments[0][0] - square_size
            new_segment_y = snake_segments[0][1]
        elif snake_direction == 'right':
            new_segment_x = snake_segments[0][0] + square_size
            new_segment_y = snake_segments[0][1]

        snake_segments.insert(0, (new_segment_x, new_segment_y))

        draw_snake(snake_segments)
        draw_pellet(pellet_color)
        draw_border_lines()
        check_snake_collision(snake_segments)

        pyg.display.flip()

        # ?? maybe the snake itself can be rounded at its head / tail? .. take up 1/2 box
         
        # ?? WE NEED TO INCLUDE AN PELLET!!!! COUNTER!!!!
        #   (WE NEED TO INCLUDE A TIMER?

        # ?? WE HAVE TO RANDOMIZE WHERE THE FIRST PELLET GOES AND WHERE THEY GO!
        #   THEY JUST CAN'T SPAWN ON TOP OF THE SNAKE

        # ?? WE NEED TO PUT BOUNDARIES SO THAT THE SNAKE CRASHES INTO WALLS / ITSELF


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # this is what should be presented SHOULD A GAME BE FINISHED!
    # 1. the results - the # of pellets
    # 2. 'play again!!'
    # 3. (settings?)
    # 4. high score: 

    pellet_counter = 17
    pellet_counter_history.append(pellet_counter)

    while end_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        pyg.display.set_caption("Final Screen")

        back_arrow()
        back_arrow_polygon_option = back_arrow()

        '''
        # this is a text layout example!!!
        title_font = pyg.font.Font(None,80)
        title_height = height//2-20
        title_title = title_font.render("testing! testing!", True, gen_col)
        title_rect = title_title.get_rect(center=(width//2, title_height))
        screen.blit(title_title, title_rect)
        # this is a text layout example!!!
        '''

        # TO PRINT PELLET ROUND INFORMATION...
        num_of_pellets = pellet_counter
        num_font = pyg.font.Font(None, 50)
        pellet_font = pyg.font.Font(None, 30)

        num_box_height = height // 2 - 100
        num_info = num_font.render(str(pellet_counter), True, gen_col)
        pellet_word = pellet_font.render("PELLETS", True, gen_col)
        num_rect = num_info.get_rect(center=(width // 2 - 10, num_box_height))
        pellet_rect = pellet_word.get_rect(center=(width // 2 + 60, num_box_height))
        screen.blit(num_info, num_rect)
        screen.blit(pellet_word, pellet_rect)


        # TO PRINT HIGH SCORE INFORMATION...



        #high_score = max(pellet_counter_history)
        #if (high_score == pellet_counter):

        # TO ASK USER IF THEY WANT TO PLAY AGAIN...

        # EVENTS CATCHER...
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
            # WHAT HAPPENS WHEN THE MOUSE IS CLICKED...
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
                if is_inside_arrow(mouse_pos, back_arrow_polygon_option):
                    game_screen = True
                    # ?? THIS IS WHERE YOU'RE HAD TO PRESENT THE RESULTS OF THE 
                    #   LAST GAME AND CAPTURE THAT MEMORY SOMEHOW... ??
                    end_screen = False
                    break
        pyg.display.flip()

pyg.quit()
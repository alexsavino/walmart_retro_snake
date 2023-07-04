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


# INITIALIZING THE GENERAL SCREEN...
pyg.init()
width, height = 640, 480
screen = pyg.display.set_mode((width,height))
gen_col = 'white'
clock = pyg.time.Clock()

# INITIALIZING SCREENS...
title_screen = False
option_screen = False
game_screen = True
end_screen = False

# TO CREATE MAC DISPLAY NAME IN THE CASE OF NO USERNAME...
round_animal_name = rand.choice(['Fox','Robin','Chipmunk','Squirrel','Deer'])
    
# INSTANTIATING THE ARRAY SQUARE PROPERTIES...
square_size = 18
row_span, col_span = (width-75),(height-100)
num_rows = col_span//square_size
num_cols = row_span//square_size

# TO POSITION THE ARRAY...
board_x = (width-(num_cols*square_size))/2
board_y = 78

# TO INSTANTIATE PELLET PROPERTIES...
pellet_x, pellet_y = 0, 0
pellet_counter = 0
pellet_counter_history = []

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# FUNCTIONS THAT RELATE THE SCREENS...
def draw_arrow(arrow_type):
    dilation = 5
    if (arrow_type == 'forward'):
        arrow_color = 'green'
        x, y = 124.5, 90
        arrow_vertices = list(dilation * np.array([(x, y), (x-3, y+2.5), (x-3, y+1.25), 
                (x-7, y+1.25), (x-7, y-1.25), (x-3, y-1.25), (x-3, y-2.5)]))
        pyg.draw.polygon(screen, arrow_color, arrow_vertices, width=2)
    elif (arrow_type == 'backward'):
        arrow_color = 'red'
        x, y = 3, 5
        arrow_vertices = list(dilation * np.array([(x, y), (x+3, y+2.5), (x+3, y+1.25), 
            (x+7, y+1.25), (x+7, y-1.25), (x+3, y-1.25), (x+3, y-2.5)]))
        pyg.draw.polygon(screen, arrow_color, arrow_vertices, width=2)
    # TO ENABLE HOVER COLOR...
    if is_inside_shape(mouse_pos, arrow_vertices):
        polygon_surface = pyg.Surface((width,height), pyg.SRCALPHA)
        pyg.draw.polygon(polygon_surface, arrow_color, arrow_vertices)
        screen.blit(polygon_surface, (0, 0))
    return arrow_vertices
    
def draw_game_control_buttons(button_type):
    dilation = 5
    x, y = 120, 2
    if (button_type == 'pause'):
        button_1_vertices = list(dilation*np.array([(x, y),(x+2, y),(x+2, y+6),(x, y+6)]))
        button_2_vertices = list(dilation*np.array([(x+3, y),(x+5, y),(x+5, y+6),(x+3, y+6)]))
        pyg.draw.polygon(screen, gen_col, button_1_vertices, width=2)
        pyg.draw.polygon(screen, gen_col, button_2_vertices, width=2)

        if is_inside_shape(mouse_pos, button_1_vertices) or is_inside_shape(mouse_pos, button_2_vertices):
            polygon_surface = pyg.Surface((width,height), pyg.SRCALPHA)
            pyg.draw.polygon(polygon_surface, 'red', button_1_vertices)
            pyg.draw.polygon(polygon_surface, 'red', button_2_vertices)
            screen.blit(polygon_surface, (0, 0))


    if (button_type == 'play'):
        button_vertices = list(dilation*np.array([(x, y+0.5),(x, y+5.5),(x+5, y+3)]))
        pyg.draw.polygon(screen, 'green', button_vertices, width=2)

        # TO ENABLE HOVER COLOR...
        if is_inside_shape(mouse_pos, button_vertices):
            polygon_surface = pyg.Surface((width,height), pyg.SRCALPHA)
            pyg.draw.polygon(polygon_surface, 'green', button_vertices)
            screen.blit(polygon_surface, (0, 0))

        return button_vertices


def is_inside_shape(point,arrow_vertices):
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


def print_center_text(font_size, text, center_coords):
    font = pyg.font.Font(None,font_size)
    title = font.render(text, True, gen_col)
    rect = title.get_rect(center=center_coords)
    screen.blit(title, rect)
    return rect

def print_topleft_text(font_size, text, topleft):
    font = pyg.font.Font(None,font_size)
    surface = font.render(text, True, gen_col)
    rect = surface.get_rect(topleft=topleft)
    screen.blit(surface, rect)
    return rect


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
            pyg.draw.rect(screen, gen_col, given_box, width=2)

    if line_identifier in hovered_colors:
        color = a_font.render(str(hovered_colors[line_identifier]), True, gen_col)
        color_bar_caption(color, q_top)

        last_hovered_box_index = color_options.index(hovered_colors[line_identifier])
        last_hovered_box_x = q_rect.right + 30 + (last_hovered_box_index * color_box_width)
        last_hovered_box_y = q_top + color_box_height_adj
        last_hovered_box = pyg.Rect(last_hovered_box_x, last_hovered_box_y, color_box_width, color_box_width)
        pyg.draw.rect(screen, gen_col, last_hovered_box, width=2)

        if (line_identifier == 'snake'):
            snake_color = hovered_colors[line_identifier]
            return snake_color
        elif (line_identifier == 'pellet'):
            pellet_color = hovered_colors[line_identifier]
            return pellet_color
        elif (line_identifier == 'board'):
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
    end_screen, game_screen = True, False


def draw_snake(snake_segments):
    for segment in snake_segments:
        x, y = segment
        pyg.draw.rect(screen, snake_color, (x, y, square_size, snake_width))

def clear_snake(snake_segments):
    for segment in snake_segments:
        x, y = segment
        pyg.draw.rect(screen, 'black', (x, y, square_size, snake_width))



def add_snake_segment(snake_segments):
    # 1. to find the direction categorize the differences in the last two squares
    # 2. then add on in the opposite direction
    horizontal_diff = snake_segments[-2][0] - snake_segments[-1][0]
    vertical_diff = snake_segments[-2][1] - snake_segments[-1][1]

    if (horizontal_diff > 0):
        segment_x = snake_segments[-1][0] + square_size
        segment_y = snake_segments[-1][1]
    elif (horizontal_diff < 0):
        segment_x = snake_segments[-1][0] - square_size
        segment_y = snake_segments[-1][1]
    elif (vertical_diff > 0):
        segment_x = snake_segments[-1][0]
        segment_y = snake_segments[-1][1] - square_size
    elif (vertical_diff < 0):
        segment_x = snake_segments[-1][0]
        segment_y = snake_segments[-1][1] + square_size
        
    snake_segments.append((segment_x,segment_y))


def get_pellet_rect():
    pellet_rect = pyg.Rect(pellet_x, pellet_y, square_size, square_size)
    return pellet_rect

# ?? HOW TO MAKE SURE THAT A PELLET DOESNST SPAWN ON THE SNAKE? ??
def draw_pellet(pellet_color,respawn=False):
    global pellet_x, pellet_y, board_x, board_y, pellet_rect

    if pellet_x == 0 and pellet_y == 0:
        pellet_x = board_x + (rand.randint(1, num_cols-1)*square_size)
        pellet_y = board_y + (rand.randint(1, num_rows-1)*square_size)

    pellet_rect = get_pellet_rect()

    # TO DRAW A BLACK BORDER AROUND THE PELLET...
    pyg.draw.line(screen, 'black', (pellet_x,pellet_y), (pellet_x+square_size,pellet_y), width=1)
    pyg.draw.line(screen, 'black', (pellet_x+square_size,pellet_y), (pellet_x+square_size,pellet_y+square_size), width=1)
    pyg.draw.line(screen, 'black', (pellet_x+square_size,pellet_y+square_size), (pellet_x,pellet_y+square_size), width=1)
    pyg.draw.line(screen, 'black', (pellet_x, pellet_y+square_size), (pellet_x,pellet_y), width=1)
    pyg.draw.rect(screen, pellet_color, pellet_rect)


def pellet_tracker(snake_segments, pellet_color):
    global pellet_counter
    global pellet_x, pellet_y
    x, y = snake_segments[0]
    snake_head_rect = pyg.Rect(x, y, square_size, square_size)
    pellet_rect = get_pellet_rect()

    if snake_head_rect.colliderect(pellet_rect):
        pellet_counter += 1
        pellet_x = board_x + (rand.randint(1, num_cols - 1) * square_size)
        pellet_y = board_y + (rand.randint(1, num_rows - 1) * square_size)
        draw_pellet(pellet_color, True)
        
        add_snake_segment(snake_segments)
    
    return pellet_counter


def draw_end_screen_pellet(pellet_color):

    pellet_rect = pyg.Rect(230, 120, square_size*2, square_size*2)

    # TO DRAW A BLACK BORDER AROUND THE PELLET...
    pyg.draw.line(screen, 'black', (pellet_x, pellet_y), (pellet_x + square_size, pellet_y), width=1)
    pyg.draw.line(screen, 'black', (pellet_x + square_size, pellet_y), (pellet_x + square_size, pellet_y + square_size), width=1)
    pyg.draw.line(screen, 'black', (pellet_x + square_size, pellet_y + square_size), (pellet_x, pellet_y + square_size), width=1)
    pyg.draw.line(screen, 'black', (pellet_x, pellet_y + square_size), (pellet_x, pellet_y), width=1)
    pyg.draw.rect(screen, pellet_color, pellet_rect)




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
    global pellet_counter
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
            pellet_counter -= 5
            if (pellet_counter <= 0):
                pellet_counter = 0
                blink_array(self_collision=True)
                end_screen, game_screen = True, False


def draw_end_screen_dec_box(board_color):
    box_height = 340
    line_1_adjustment = 50
    box_width = width - 2 * line_1_adjustment

    # Calculate the x-coordinate of the box
    box_x = (width - box_width) // 2
    # Calculate the y-coordinate of the box
    box_y = 80

    # Top line coordinates with adjustments
    line_1_start = box_x
    line_1_end = box_x + box_width
    line_1 = (line_1_start, box_y - 1, line_1_end, box_y - 1)
    # Left line coordinates
    line_2 = (box_x - 1, box_y, box_x - 1, box_y + box_height - 3)
    # Right line coordinates
    line_3 = (box_x + box_width + 1, box_y, box_x + box_width + 1, box_y + box_height - 3)
    # Bottom line coordinates
    line_4 = (box_x, box_y + box_height - 2, box_x + box_width, box_y + box_height - 2)

    pyg.draw.line(screen, board_color, line_1[0:2], line_1[2:4], width=1)
    pyg.draw.line(screen, board_color, line_2[0:2], line_2[2:4], width=1)
    pyg.draw.line(screen, board_color, line_3[0:2], line_3[2:4], width=1)
    pyg.draw.line(screen, board_color, line_4[0:2], line_4[2:4], width=1)
















#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# PRIMARY GAME LOOP...
while True:

    SPACE_timer = 0

    while title_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        pyg.display.set_caption("Snake Game")

        # TO MAKE THE TITLE + SUBTITLE...
        print_center_text(80, "SNAKE GAME", (width//2, height//2-20))
        print_center_text(30, "PRESS                TO START", (width//2, height//2+25))

        # TO MAKE THE 'SPACE' BLINK...
        SPACE_visible = True
        SPACE_timer += 1
        time_not_visible, time_visible = 825, 700

        if (SPACE_timer > time_visible) and (SPACE_timer < time_not_visible):
            SPACE_visible = not SPACE_visible
        elif SPACE_timer >= time_not_visible:
            SPACE_timer = 0

        if SPACE_visible:
            print_topleft_text(35, "SPACE", (width//2-54, height//2+12))

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

    while option_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        pyg.display.set_caption("Game Settings")
        draw_end_screen_dec_box(gen_col)

        # TO CREATE SCREEN-BUTTONS!
        back_arrow_polygon_option = draw_arrow('backward')
        forward_arrow_polygon_option = draw_arrow('forward')

        # SCREEN TITLE...
        print_center_text(50, "GAME SETTINGS", (width//2,46))

        space_between_questions = 88
        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 1: NAME

        q_font = pyg.font.Font(None, 25)
        a_font = pyg.font.Font(None, 22)

        name_question = "1. WHAT'S YOUR NAME?: "
        username = ""

        # TO POSITION BOTH QUESTION / ANSWER...
        q_left, q_top = 75, 100
        q_surface = q_font.render(name_question, True, gen_col)
        q_rect = q_surface.get_rect(topleft=(q_left, q_top))
        screen.blit(q_surface, q_rect)

        #print_topleft_text(25, "1. WHAT'S YOUR NAME?: ", (q_left, q_top))

        a_top, a_left = (q_top+1.5), (q_rect.right+3)
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
        snake_q_rect = print_topleft_text(25, "2. SNAKE COLOR?: ", (snake_q_left,snake_q_top))
        color_bar_system(snake_q_rect,snake_q_top,'snake')

        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 4: PELLET COLOR
        pellet_q_left, pellet_q_top = q_left, (snake_q_top+space_between_questions)
        pellet_q_rect = print_topleft_text(25, "3. PELLET COLOR?: ", (pellet_q_left,pellet_q_top))
        color_bar_system(pellet_q_rect,pellet_q_top,'pellet')

        #------------------------------------------------------------------------------------------------------------------
        # PREFERENCE 3: BOARD COLOR
        board_q_left, board_q_top = q_left, (pellet_q_top+space_between_questions)
        board_q_rect = print_topleft_text(25, "4. BOARD COLOR?: ", (board_q_left,board_q_top))
        color_bar_system(board_q_rect,board_q_top,'board')


        # EVENTS CATCHER...
        for event in pyg.event.get():
            if (event.type == pyg.QUIT):
                pyg.quit()
            # TO ENTER USERNAME...
            elif (event.type == KEYDOWN):
                if (event.key == K_BACKSPACE):
                    username = username[:-1]
                elif event.unicode.isalpha() or event.unicode.isspace():
                    if (event.unicode != '\t') and (event.key != 13) and (len(username) < 20):
                        username += event.unicode
            # WHAT HAPPENS WHEN THE MOUSE IS CLICKED...
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
                if is_inside_shape(mouse_pos, back_arrow_polygon_option):
                    title_screen, option_screen = True, False
                    break
                # WHAT HAPPENS IF FORWARD BUTTON IS PRESSED...
                elif is_inside_shape(mouse_pos, forward_arrow_polygon_option):
                    game_screen, option_screen = True, False
                    break

        pyg.display.flip()

    #username = username.strip()

# ?? HOW TO MAKE IT SO THAT SOMEONE'S NAME STAYS EVEN AS YOU 
#    GO BACK AND FORTH BETWEEN OPTION AND GAME SCREENS??

# ?? maybe i can make it so that when you do hit enter on your name quotes appear? 
#   maybe a color change? put a white box around it? something to differentiate
#   how could you go back and edit it yourself?


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # TO CREATE MAC DISPLAY NAME IN THE CASE OF NO USERNAME...
    anonymous_username = pyg.display.set_caption("Anonymous {}'s Snake Game".format(round_animal_name))
                                                 
    board_color = 'PURPLE' # !! PLACEHOLDER !! ... supposed to be 'board_color'
    snake_color = 'BLUE' # TEST_SNAKE_COLOR
    pellet_color = 'RED' #TEST_PELLET_COLOR

    # TO INSTANTIATE THE SNAKE...
    snake_box_length = 3 
    snake_length = snake_box_length * square_size
    snake_width = square_size

    snake_x = board_x+(10*square_size)
    snake_y = board_y+(10*square_size)
    snake_direction = 'right'
    snake_segments = []

    for square in range(snake_box_length):
        segment_x = snake_x-(snake_box_length-square)*square_size
        segment_y = snake_y
        snake_segments.append((segment_x,segment_y))

    snake_segments = snake_segments[::-1]

    # TO DETERMINE BOTH BOARD COLORS...
    board_colors = [['red','tomato'],['chocolate','orange'],['gold','yellow'],
        ['green','limegreen'],['blue','royalblue'],['darkviolet','mediumorchid']]
    board_color_1 = board_colors[color_options.index(board_color)][0]
    board_color_2 = board_colors[color_options.index(board_color)][1]
    
    pellet_counter = 0

    while game_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        clock.tick(10)

        # TO CREATE MAC DISPLAY NAME...
        username = "" # !! PLACEHOLDER !!
        if username == "":
            anonymous_username
        else:
            pyg.display.set_caption("{}'s Snake Game".format(username))

        # TO CREATE SCREEN BUTTONS / SCREEN TITLE / ARRAY / SNAKE...
        back_arrow_polygon_option = draw_arrow('backward')
        print_center_text(50, "SNAKE GAME...", (width//2-118,54))
        draw_array(board_color_1,board_color_2)
        draw_border_lines()
        snake_segments.pop()


        pellet_counter = pellet_tracker(snake_segments, pellet_color)
        if (len(str(pellet_counter)) == 1):
            print_center_text(38, str(pellet_counter), (width//2+155,59))
        elif (len(str(pellet_counter)) == 2):
            print_center_text(38, str(pellet_counter), (width//2+150,59))
        print_center_text(25, "PELLETS", (width//2+210,60))


        # once you click on this shape your entire screen gets a little darker and the shape itself
        # changes into that play triangle ** 

        # EVENTS CATCHER...
        for event in pyg.event.get():
            if (event.type == pyg.QUIT):
                pyg.quit()
            # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                if is_inside_shape(mouse_pos, back_arrow_polygon_option):
                    option_screen, game_screen = True, False
                    break
            
            elif event.type == KEYDOWN:
                if (event.key == pyg.K_UP) and (snake_direction != 'down'):
                    snake_direction = 'up'
                elif (event.key == pyg.K_DOWN) and (snake_direction != 'up'):
                    snake_direction = 'down'
                elif (event.key == pyg.K_LEFT) and (snake_direction != 'right'):
                    snake_direction = 'left'
                elif (event.key == pyg.K_RIGHT) and (snake_direction != 'left'):
                    snake_direction = 'right'

        # TO CALCULATE NEW HEAD SQUARE + SHIFT UP OTHER SQUARES...
        if (snake_direction == 'up'):
            new_segment_x = snake_segments[0][0]
            new_segment_y = snake_segments[0][1]-square_size
        elif (snake_direction == 'down'):
            new_segment_x = snake_segments[0][0]
            new_segment_y = snake_segments[0][1]+square_size
        elif (snake_direction == 'left'):
            new_segment_x = snake_segments[0][0]-square_size
            new_segment_y = snake_segments[0][1]
        elif (snake_direction == 'right'):
            new_segment_x = snake_segments[0][0]+square_size
            new_segment_y = snake_segments[0][1]
        snake_segments.insert(0, (new_segment_x,new_segment_y))

        draw_snake(snake_segments)
        draw_pellet(pellet_color)
        check_snake_collision(snake_segments)
        #draw_game_control_buttons('play')
        draw_game_control_buttons('pause')
        pyg.display.flip()

        # ?? maybe the snake itself can be rounded at its head / tail? .. take up 1/2 box

        # ?? HOW TO DO A PAUSE BUTTON ??

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    pellet_counter_history.append(pellet_counter)

    while end_screen:
        screen.fill('black')
        mouse_pos = pyg.mouse.get_pos()
        pyg.display.set_caption("Final Screen")

        back_arrow_polygon_option = draw_arrow('backward')
        # ?? if you hit the back button all you see is ur dead snake unable to move.. ?? 

        draw_end_screen_pellet(pellet_color)
        draw_end_screen_dec_box(board_color)

        # TO PRINT PELLET ROUND INFO / HIGH SCORE INFO / ...
        if (pellet_counter == 1):
            print_center_text(50, str(pellet_counter), (width//2-23,height//2-100))
            print_center_text(30, "PELLET", (width//2+43,height//2-100))
        else: 
            print_center_text(50, str(pellet_counter), (width//2-25,height//2-100))
            print_center_text(30, "PELLETS", (width//2+45,height//2-100))

        if max(pellet_counter_history) >= 100:
            print_center_text(57, str(max(pellet_counter_history)), (width//2+105,height//2-24))
            print_center_text(50, "High Score: ", (width//2-33,height//2-24))
        else:
            print_center_text(57, str(max(pellet_counter_history)), (width//2+100,height//2-20))
            print_center_text(50, "High Score: ", (width//2-25,height//2-20))

        # TO PRINT PLAY AGAIN OPTION...
        play_again_rect = print_center_text(70, "PLAY AGAIN?", (width//2, height//2+85))
        inner_rect = pyg.Rect(play_again_rect.left-10, play_again_rect.top-15, play_again_rect.width+18, play_again_rect.height+20)
        pyg.draw.rect(screen, gen_col, inner_rect, width=1)
        play_again_vertices = [(inner_rect.left, inner_rect.top), (inner_rect.right, inner_rect.top), 
            (inner_rect.right, inner_rect.bottom), (inner_rect.left, inner_rect.bottom)]

        # EVENTS CATCHER...
        for event in pyg.event.get():
            if (event.type == pyg.QUIT):
                pyg.quit()
            # WHAT HAPPENS WHEN THE MOUSE IS CLICKED...
            elif (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                # WHAT HAPPENS IF BACK-BUTTON IS PRESSED...
                if is_inside_shape(mouse_pos, back_arrow_polygon_option):
                    game_screen, end_screen = True, False
                    break
                elif is_inside_shape(mouse_pos, play_again_vertices):
                    option_screen, end_screen = True, False
                    break

        pyg.display.flip()

pyg.quit() # ?? should this be tabbed in one? ?? 
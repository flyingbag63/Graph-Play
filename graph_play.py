import sys,os,time
import pygame
from pygame.locals import *
from Graph import Graph
from Options import Options
from Circle import Circle

def initialize(SCREEN_SIZE,BLACK,screen):
    ROWS = SCREEN_SIZE[1]

    #initializing game objects
    graph = Graph()
    options = Options(SCREEN_SIZE)
    COLS = options.get_options_column_size(SCREEN_SIZE)
    circle = Circle(ROWS,COLS)

    #Fill Background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(BLACK)
    
    #options bar
    options.display_options(background,SCREEN_SIZE)

    #blit background on screen
    screen.blit(background,(0,0))
    pygame.display.flip()

    drawing = False         #whether mouse button gets pressed or not
    frame_rate = 0
    curr_time = time.time()
    playing = True

    return options,graph,ROWS,COLS,circle,background,drawing,frame_rate,curr_time,playing

def main():
    #constants
    SCREEN_SIZE = (800,600)
    BLACK  = (0,0,0)
    
    #initializing game environment
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Graph Play')

    options,graph,ROWS,COLS,circle,background,drawing,frame_rate,curr_time,playing = initialize(SCREEN_SIZE,BLACK,screen)

    #main game loop
    while playing:
        rect_objects_to_update = []
        frame_rate += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False

        #print frame rate on screen
        if time.time()-curr_time >= 1:
            #print(frame_rate)
            frame_rate = 0
            curr_time = time.time()

            
        if options.is_option_chosen:
            drawing,rect_objects = options.choose_option(screen,drawing,ROWS,COLS,pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0],graph,circle=circle)
            if rect_objects:
                rect_objects_to_update.extend(rect_objects)
        else:
            drawing,circle_rect_obj = circle.draw_circle(screen,drawing,ROWS,COLS,pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0],graph)
            if circle_rect_obj:
                rect_objects_to_update.append(circle_rect_obj)

            drawing,rect_objects = options.choose_option(screen,drawing,ROWS,COLS,pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0],graph,circle=circle)
            if rect_objects:
                rect_objects_to_update.extend(rect_objects)

        #update the screen with new Rectangle objects 
        pygame.display.update(rect_objects_to_update)
        if options.new:
            options,graph,ROWS,COLS,circle,background,drawing,frame_rate,curr_time,playing = initialize(SCREEN_SIZE,BLACK,screen)

    #print(graph.edges)
    pygame.quit()


if __name__ == "__main__":
    main()

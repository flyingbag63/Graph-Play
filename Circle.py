import pygame
from pygame.locals import *

class Circle:

    def __init__(self,rows,cols):
        self.radius = 20
        self.color = (255,255,255)
        self.nodes_array = [[-1 for j in range(rows)] for i in range(cols)]         #array respresenting the center of circle, that position has if any
        self.selected = []                                                          #array representing selected circles
        self.selected_color = (255,189,0)                                           #color of a selected circle
        self.original_colors = {}                                                   #denotes original color of nodes and edges, which can be used to reset
        self.total = 0

    def select_circles(self,n,screen,drawing,ROWS,COLS,mouse_pos,button_pressed,color=None):
        '''function to select n circles based on mouse position'''
        circle_rect_obj = None
        if len(self.selected) < n:
            if not color:
                drawing,circle_rect_obj = self.draw_circle(screen,drawing,ROWS,COLS,mouse_pos,button_pressed,None,self.selected_color,first_time=False)
            else:
                drawing,circle_rect_obj = self.draw_circle(screen,drawing,ROWS,COLS,mouse_pos,button_pressed,None,color,first_time=False)
            if circle_rect_obj:
                self.selected.append(circle_rect_obj.center)
                if not color:
                    self.original_colors[mouse_pos] = self.selected_color

        return drawing,circle_rect_obj

    def draw_line(self,screen,start,end,color=None):
        if not color:
            color = self.selected_color
            self.original_colors[(start,end)] = color
            
        line = pygame.draw.line(screen,color,start,end)
        return line

    def can_draw(self,screen,mouse_pos,ROWS,COLS):
        x,y = mouse_pos
        left_x = x-self.radius
        right_x = x+self.radius
        up_y = y-self.radius
        down_y = y+self.radius

        #check out of boundary conditions
        if left_x < 0 or right_x >= COLS or up_y < 0 or down_y >= ROWS:
            return False

        #check if any pixel in the area of current circle is WHITE
        for x in range(left_x,right_x+1):
            for y in range(up_y,down_y+1):
                if tuple(screen.get_at((x,y)))[:3] in [self.color,self.selected_color]:
                    return False

        return True

    def fill_array(self,mouse_pos):
        x,y = mouse_pos
        left_x = x-self.radius
        right_x = x+self.radius
        up_y = y-self.radius
        down_y = y+self.radius

        #fill the smallest square containing the circle with circle center
        for x in range(left_x,right_x+1):
            for y in range(up_y,down_y+1):
                #print(x,y)
                self.nodes_array[x][y] = mouse_pos

    def draw_circle(self,screen,drawing,ROWS,COLS,mouse_pos,button_pressed,graph,color=None,first_time=True):
        if not color:
            color = self.color
            
        #first_time represents whether the circle is being drawn for the first time on screen
        circle_rect_obj = None
        if drawing:
            #if mouse button gets unpressed
            if not button_pressed:
                drawing = False 
        else:
            #if left mouse button gets pressed, get mouse position and draw a circle
            if button_pressed:
                drawing = True
                if first_time:
                    if self.can_draw(screen,mouse_pos,ROWS,COLS):
                        circle_rect_obj = pygame.draw.circle(screen,color,mouse_pos,self.radius)
                        self.original_colors[mouse_pos] = color
                        graph.add_node(mouse_pos)
                        self.fill_array(mouse_pos)
                        self.total += 1
                else:
                    #get center of circle
                    x,y = mouse_pos
                    if x < ROWS and y < COLS:
                        mouse_pos = self.nodes_array[x][y]
                        if mouse_pos != -1:
                            circle_rect_obj = pygame.draw.circle(screen,color,mouse_pos,self.radius)

        return drawing,circle_rect_obj

import time,pygame,random

class Options:
    def __init__(self,screen_size):
        self.options = ['Reset',
                        'New',
                        'Add Edge',
                        'Shortest Path',
                        'BFS',
                        'DFS',
                        'Connected Components',
                        'Cycles',
                        #'MST'
                        ]
        self.font_type = 'Comic Sans MS'                                                                #type of font used for options menu
        self.font_color = (255,189,0)                                                                   #color of font used for options menu
        self.percent_columns_occupied = 0.25                                                            #percentage of columns occupied by options menu from the right side of screen
        self.column_gap_percent = 0.01                                                                  #percentage of columns to be left from left and right
        self.row_gap_percent = 0.10                                                                     #percentage of rows to be left from up and down
        self.options_array = [['' for j in range(screen_size[1])] for i in range(screen_size[0])]       #array representing the option number an area is covering, if any
        self.is_option_chosen = False                                                                   #boolean representing whether any option is currently chosen or not
        self.option_chosen = ''                                                                         #which option is currently chosen
        self.selected_color = (0, 193, 255)                                                             #color denoting the circle or edge which is currently being processed by the
                                                                                                        #algorithm
        self.reset = False                                                                              #dummy variable to reset all the nodes and edges after visualizing
                                                                                                        #the order and before visualizing final_path
        self.option_done = False                                                                        #one time variable for zero node options to just call their respective
                                                                                                        #algorithm to get order and path
        self.need_to_reset = False                                                                      #boolean to denote whether there is a need to reset the colors of edges
                                                                                                        #and nodes, used after completing visualization of an option
        self.chosen_color_for_cycles = self.selected_color
        self.new = False


    def get_random_color(self):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        self.chosen_color_for_cycles = (r,g,b)

    def perform_reset(self,graph,circle,screen,ROWS,COLS):
        original_circles = []
        for i in circle.original_colors:
            if isinstance(i[0],int):
                drawing,rect_obj = circle.draw_circle(screen,False,ROWS,COLS,i,1,None,color=circle.original_colors[i],first_time=False)
            else:
                rect_obj = circle.draw_line(screen,i[0],i[1],circle.original_colors[i])
                
            original_circles.append(rect_obj)

        return original_circles

    def perform_algorithm(self,graph,circle,screen,ROWS,COLS):
        if self.option_chosen in ['Cycles','Connected Components']:
            color = self.chosen_color_for_cycles
        else:
            color = self.selected_color
        if graph.order:
            curr = graph.order.pop(0)
            #print(curr,'order')
            if isinstance(curr,str):
                self.get_random_color()
                return False,[None]
            else:
                time.sleep(0.1)
                if len(curr) == 1:
                    drawing,rect_obj = circle.draw_circle(screen,False,ROWS,COLS,curr[0],1,None,color=color,first_time=False)
                else:
                    rect_obj = circle.draw_line(screen,curr[0],curr[1],color)

            return False,rect_obj
        else:
            #print('here')
            if not self.reset:
                original_circles = self.perform_reset(graph,circle,screen,ROWS,COLS)
                self.reset = True
                return False,original_circles
            else:
                #print(graph.final_path,'here')
                if graph.final_path:
                    curr = graph.final_path.pop(0)
                    #print(curr,'final')
                    if isinstance(curr,str):
                        self.get_random_color()
                        return False,[None]
                    else:
                        time.sleep(0.1)
                        if len(curr) == 1:
                            drawing,rect_obj = circle.draw_circle(screen,False,ROWS,COLS,curr[0],1,None,color=color,first_time=False)
                        else:
                            rect_obj = circle.draw_line(screen,curr[0],curr[1],color)

                    return False,rect_obj
                else:
                    self.reset = False
                

        return False,None
            
    def fill_array(self,text_size,center,option):
        '''function to fill array with option of an area.'''
        w,h = text_size
        centerx,centery = center
        left_x = centerx-w//2
        right_x = centerx+w//2
        up_y = centery-h//2
        down_y = centery+h//2
        for x in range(left_x,right_x+1):
            for y in range(up_y,down_y+1):
                self.options_array[x][y] = option
    
    def get_options_column_size(self,SCREEN_SIZE):
        return int((1-self.percent_columns_occupied-2*self.column_gap_percent)*SCREEN_SIZE[0]) 

    def choose_option(self,screen,drawing,ROWS,COLS,mouse_pos,button_pressed,graph,circle=None):
        '''function to choose option, if any and visualize related algorithm'''
        rect_objects = []
        
        if self.need_to_reset:
            if button_pressed:
                x,y = mouse_pos
                if self.options_array[x][y]:
                    self.option_chosen = self.options_array[x][y]
                    self.is_option_chosen = True
                    
            if not self.is_option_chosen:
                return False,None
            
            if self.option_chosen != 'Reset':
                self.is_option_chosen = False
                return False,None

            self.is_option_chosen = False
            self.need_to_reset = False
            self.option_chosen = ''
            original_circles = self.perform_reset(graph,circle,screen,ROWS,COLS)

            return False,original_circles
        
        if not self.is_option_chosen:
            if button_pressed:
                x,y = mouse_pos
                if self.options_array[x][y]:
                    self.option_chosen = self.options_array[x][y]
                    self.is_option_chosen = True
        else:
            two_node_options = ['Add Edge','Shortest Path']
            one_node_options = ['BFS','DFS']
            zero_node_options = ['Reset','New','Connected Components','Cycles','MST']
                
            if self.option_chosen in zero_node_options:
                if not self.option_done:
                    self.option_done = True
                    if self.option_chosen == 'Connected Components':
                        graph.connected_components()
                    elif self.option_chosen == 'Cycles':
                        graph.cycles()
                    elif self.option_chosen == 'Reset':
                        original_circles = self.perform_reset(graph,circle,screen,ROWS,COLS)
                        self.is_option_chosen = False
                        self.need_to_reset = False
                        self.option_done = False
                        self.option_chosen = ''
                        self.reset = False
                        self.curr_node_chosen_for_cycles = None
                        return False,original_circles
                    elif self.option_chosen == 'New':
                        self.new = True
                        return False,None
                else:
                    drawing,rect_obj = self.perform_algorithm(graph,circle,screen,ROWS,COLS)
                    if rect_obj:
                        if not isinstance(rect_obj,list):
                            rect_objects.append(rect_obj)
                        else:
                            rect_objects.extend(rect_obj)
                    else:
                        self.is_option_chosen = False
                        self.need_to_reset = True
                        self.option_done = False
                        self.option_chosen = ''
                        self.reset = False
                        self.curr_node_chosen_for_cycles = None
                        return False,None
                    
            elif self.option_chosen in one_node_options:
                if circle.total < 1:
                    self.is_option_chosen = False
                    self.option_chosen = ''
                    return False,None
                #print(circle.selected)
                if len(circle.selected) == 1:
                    if self.option_chosen in ['BFS','DFS']:
                        drawing,rect_obj = self.perform_algorithm(graph,circle,screen,ROWS,COLS)
                        if rect_obj:
                            if not isinstance(rect_obj,list):
                                rect_objects.append(rect_obj)
                            else:
                                rect_objects.extend(rect_obj)
                        else:
                            self.is_option_chosen = False
                            self.need_to_reset = True
                            self.option_done = False
                            self.option_chosen = ''
                            self.reset = False
                            self.curr_node_chosen_for_cycles = None
                            circle.selected = []
                else:
                    drawing,rect_object = circle.select_circles(1,screen,drawing,ROWS,COLS,mouse_pos,button_pressed,self.selected_color)
                    rect_objects.append(rect_object)
                    if len(circle.selected) == 1:
                        if self.option_chosen == 'BFS': 
                            graph.bfs(circle.selected[0])
                        elif self.option_chosen == 'DFS':
                            graph.dfs(circle.selected[0])
                    
            elif self.option_chosen in two_node_options:
                if circle.total < 2:
                    self.is_option_chosen = False
                    self.option_chosen = ''
                    return False,None
                if len(circle.selected) == 2:
                    if self.option_chosen == 'Add Edge':
                        #TODO take edge weight from user as input
                        graph.add_edge(circle.selected[0],circle.selected[1])
                        rect_object = circle.draw_line(screen,circle.selected[0],circle.selected[1])
                        self.option_chosen = ''
                        self.is_option_chosen = False
                        circle.selected = []
                        rect_objects.append(rect_object)
                    else:
                        drawing,rect_obj = self.perform_algorithm(graph,circle,screen,ROWS,COLS)
                        if rect_obj:
                            if not isinstance(rect_obj,list):
                                rect_objects.append(rect_obj)
                            else:
                                rect_objects.extend(rect_obj)
                        else:
                            self.is_option_chosen = False
                            self.need_to_reset = True
                            self.option_done = False
                            self.option_chosen = ''
                            self.reset = False
                            self.curr_node_chosen_for_cycles = None
                            circle.selected = []
                else:
                    if self.option_chosen == 'Add Edge':
                        drawing,rect_object = circle.select_circles(2,screen,drawing,ROWS,COLS,mouse_pos,button_pressed)
                    else:
                        drawing,rect_object = circle.select_circles(2,screen,drawing,ROWS,COLS,mouse_pos,button_pressed,color=self.selected_color)
                        
                    rect_objects.append(rect_object)
                    if len(circle.selected) == 2:
                        if self.option_chosen == 'Shortest Path':
                            graph.shortest_path(circle.selected[0],circle.selected[1])

        return drawing,rect_objects

    def get_max_width_and_height(self,size):
        '''helper function to get max width and total height occupied by all options given the size'''
        
        max_width = 0
        total_height = 0
        for option in self.options:
            font = pygame.font.SysFont(self.font_type,size)
            w,h = font.size(option)
            max_width = max(max_width,w)
            total_height += h

        return max_width,total_height

    def find_optimal_size_and_centerx_and_gap_bet_rows(self,SCREEN_SIZE):
        '''function to get optimal size of font, centerx of font rect and optimal gap between successive options'''
        
        width,height = SCREEN_SIZE
        columns_occupied = int(self.percent_columns_occupied*width-2*self.column_gap_percent*width)
        low = 0
        high = columns_occupied
        optimal_size = -1
        
        #binary search on the optimal size of the font
        while low <= high:
            mid = (low+high)//2
            max_width,total_height = self.get_max_width_and_height(mid)
            if max_width <= columns_occupied:
                low = mid+1
                optimal_size = mid
            else:
                high = mid-1

        max_width,total_height = self.get_max_width_and_height(optimal_size)
        centerx = int((1-self.percent_columns_occupied)*width+((max_width+2*self.column_gap_percent*width)/2))
        rows_occupied = height-2*self.row_gap_percent*height
        row_gap = int((rows_occupied-total_height)/len(self.options))
        height = total_height//len(self.options)

        return optimal_size,centerx,row_gap,height
            

    def display_options(self,background,SCREEN_SIZE):
        '''function to display options side bar'''

        startx = endx = int((1-self.percent_columns_occupied-2*self.column_gap_percent)*SCREEN_SIZE[0])
        starty = 0
        endy = SCREEN_SIZE[1]
        pygame.draw.line(background,self.font_color,(startx,starty),(endx,endy))
        size,centerx,row_gap,height = self.find_optimal_size_and_centerx_and_gap_bet_rows(SCREEN_SIZE)
        centery = int(self.row_gap_percent*SCREEN_SIZE[1]+(height/2))
        for option in self.options:
            font = pygame.font.SysFont(self.font_type,size)
            text = font.render(option,False,self.font_color)
            textpos = text.get_rect(center=(centerx,centery))
            self.fill_array(textpos.size,(centerx,centery),option)
            background.blit(text,textpos)
            centery += row_gap+height

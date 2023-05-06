"""     Joshua Mahurien
        1/18/2023
        Finding Rectangles in size m*n walled maze with rigid walls
        """
#Libraries     
import random
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy
import numpy as np
import statsmodels.api as sm
from collections import defaultdict

#Globals
directions = {0:('unassigned',0,0,'black'),
              1:('left',-1,0,'blue'),
              2:('up',0,1,'green'),
              3:('right',1,0,'yellow'),
              4:('down',0,-1,'red')}


class Post:
    def __init__(self,direction,position):
        self.direction = direction
        self.position = position
        self.end_position = position
        
        
    def get_direction(self):
        return directions[self.direction]
    
    def change_end_position(self):
        self.end_position = (self.position[0]-directions[self.direction][2],
                             self.position[1]+directions[self.direction][1])
        
    
class Maze:
    def __init__(self,height,width):
        self.height = abs(int(height))
        self.width = abs(int(width))
        self.posts = self.initiate_posts()
        self.number_of_walls = (self.height-1)*(self.width-1)
        self.solution_tree = None
        self.quickest_path = None
        self.tree_count = None
        
    def initiate_posts(self):
        post_space = (self.height-1,self.width-1)
        post_array = list()
        
        #Creating posts for maze with no value, but a rectangular position
        for row in range(post_space[0]):
            post_array.append([])
            for column in range(post_space[1]):
                post_array[row].append(Post(0,(row,column)))
        return post_array
    
    def get_positional_points(self):
        positional_points = []
        for row in range(self.height):
            for column in range(self.width):
                positional_points.append((row,column))
                
        return positional_points

    def numeric_maze_directions(self):
        #Creating a matrix of posts' directions
        posts_list = list()
        for row in range(len(self.posts)):
            posts_list.append([])
            for post in self.posts[row]:
                posts_list[row].append(post.direction)
        return posts_list
    
    def check_for_cross(self,row,column):
        posts = self.numeric_maze_directions()
        current_post = posts[row][column]
        directions_to_check = [(0, -1), (-1, 0)]
        for dr, dc in directions_to_check:
            if row + dr < 0 or column + dc < 0:
                continue
            post = posts[row + dr][column + dc]
            if directions[current_post][0] == 'left' and directions[post][0] == 'right':
                return True
            elif directions[current_post][0] == 'up' and directions[post][0] == 'down':
                return True
        return False
    
    def check_for_cycle(self,row,column):
        cycle = False
        post = self.posts[row][column]
        next_post = post.end_position
        traveling = True
        #Keeping track of visited posts, if a post has been revisited, then a cycle occured
        visited = set(post.position)
        while not cycle:
            #If the destination of current post is maze perimeter, tree terminates
            if next_post[0] in [-1,self.height-1] or next_post[1] in [-1,self.width-1]:
                break
            #If the destination is a post that is unassigned a direction, tree grows
            if directions[self.posts[next_post[0]][next_post[1]].direction][0] == 'unassigned':
                break
            visited.add(next_post)
            next_post = self.posts[next_post[0]][next_post[1]].end_position
            #If the post has been visited during this path already
            if next_post in visited:
                cycle = True
        return cycle
            
    def check_wall_validity(self,row,column):
        invalid_wall = False
        cross = self.check_for_cross(row, column)
        if cross:
            return True
        cycle = self.check_for_cycle(row, column)
        if cycle:
            return True
        return invalid_wall
            
    def check_for_walls(self,point):
        walls = {"right":[False,(0,1)],
                 "below":[False,(1,0)]}
        #Checking Right Wall
        
        if point[1] < self.width-1:
            if point[0] < self.height-1:
                if self.posts[point[0]][point[1]].get_direction()[0] == 'up':
                    walls["right"][0] = True
                if point[0] != 0:
                    if self.posts[point[0]-1][point[1]].get_direction()[0] == 'down':
                        walls["right"][0] = True
            else:
                if self.posts[point[0]-1][point[1]].get_direction()[0] == 'down':
                    walls["right"][0] = True
        #Checking Below Wall
        if point[0] < self.height-1:
            if point[1] < self.width-1:
                if self.posts[point[0]][point[1]].get_direction()[0] == 'left':
                    walls['below'][0] = True
                    return walls
                if point[1] != 0:
                    if self.posts[point[0]][point[1]-1].get_direction()[0] == 'right':
                        walls['below'][0] = True
                        return walls
            else:
                if self.posts[point[0]][point[1]-1].get_direction()[0] == 'right':
                    walls['below'][0] = True
        
                
        return walls
            
    def maze_solution_tree(self):
        
        positional_points = self.get_positional_points()
        
        solution_tree_edges = [[(-1,0),(0,0)],
                               [(self.height-1,self.width-1),
                                (self.height,self.width-1)]]
        for point in positional_points:
            walls = self.check_for_walls(point)
            for wall in walls:
                if walls[wall][0] == False:
                    not_last_row =(point[0]+walls[wall][1][0]) < self.height
                    not_last_column =(point[1]+walls[wall][1][1]) < self.width
                    
                    if not_last_row and not_last_column:
                        end_row = point[0]+walls[wall][1][0]
                        end_column = point[1]+walls[wall][1][1]
                        solution_tree_edges.append([point,
                                                    (end_row,
                                                     end_column)])
            
        return solution_tree_edges
    
    def trim_tree(self,node,tree):
        for edge in tree:
            if node in edge:
                tree.remove(edge)
        return tree
    
    def check_leaf(self,node,tree):
        node_use_count = 0
        for edge in tree:
            if node in edge:
                node_use_count += 1
        if node_use_count <= 1:
            return True
        
    
    def trim_leaf(self,node,tree):
        if self.check_leaf(node,tree):
            return self.trim_tree(node,tree)
        return tree
            
            
    def maze_quickest_path(self,solution_tree):
        positional_points = self.get_positional_points()
        new_tree = solution_tree
        finding_path = True
        while finding_path:
            tree_size = len(new_tree)
            for node in positional_points:
                new_tree = self.trim_leaf(node,new_tree)
            if len(new_tree) == tree_size:
                finding_path = False
        return new_tree
            
    def count_trees(self):
        walls = np.array(self.posts).flatten()
        trees = [sum([1 for wall in walls if wall.end_position[0] in [self.height-1,-1]]),
                 sum([1 for wall in walls if wall.end_position[1] in [self.width-1,-1]]),
                 0]
        trees[2] = trees[0]+trees[1]
        self.tree_count = trees
    
    def randomize_maze(self):
        total_posts = (self.width - 1) * (self.height - 1)
        for i, row in enumerate(self.posts):
            for j, post in enumerate(row):
                current_post_number = (i * (self.width - 1)) + j + 1
                checked_walls = set()
                post.direction = random.randint(1, 4)
                checked_walls.add(post.direction)
                post.change_end_position()
                invalid_wall = self.check_wall_validity(i, j)
                while invalid_wall:
                    post.direction = random.randint(1, 4)
                    if post.direction not in checked_walls:
                        checked_walls.add(post.direction)
                        post.change_end_position()
                        invalid_wall = self.check_wall_validity(i, j)
        self.solution_tree = self.maze_solution_tree()
        copy_tree = copy.copy(self.solution_tree)
        self.quickest_path = self.maze_quickest_path(copy_tree)
        self.count_trees()
        
    def mass_randomize_data(self,n):
        maze_data = {"trees":[],
                     "left":[],
                     "right":[],
                     "solution path length":[]}
        checked_mazes = []
        i = 0
        while i < n:
            self.randomize_maze()
            post_list = self.numeric_maze_directions()
            if post_list in checked_mazes:
                continue
            i+=1
            checked_mazes.append(self.numeric_maze_directions())
            trees = self.count_trees()
            maze_data["trees"].append(self.tree_count[2])
            maze_data["left"].append(self.tree_count[0])
            maze_data["right"].append(self.tree_count[1])
            maze_data["solution path length"].append(len(self.quickest_path))
            
            
        return maze_data
    
class Maze_Aggregate:
    def __init__(self,length,width):
        self.length = length
        self.width = width
        
    def mass_randomize_data(self,n):
        maze_dict = {"trees":[],
                     "left":[],
                     "right":[],
                     "solution path length":[]}
        checked_mazes = set()
        for m in range(n):
            maze = Maze(self.length,self.width)
            maze.randomize_maze()

            trees = maze.count_trees()
            maze_dict["trees"].append(maze.tree_count[2])
            maze_dict["left"].append(maze.tree_count[0])
            maze_dict["right"].append(maze.tree_count[1])
            maze_dict["solution path length"].append(len(maze.quickest_path))
            
        return maze_dict
                
                    
            
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.maze = None
        self.create_widgets()
        self.padding = 15
        
    def create_widgets(self):
        
        #Variable lengths
        self.canvasHeight = 500
        self.canvasWidth = 500
        left_frame_widgets = []
        right_frame_widgets = []
        
        #Frame Building
        self.right_tab_control = Notebook(self.master)
        self.right_frame_data = Frame(self.right_tab_control,
                                width = self.canvasWidth + 10,
                                height = self.canvasHeight + 10)
        self.right_frame = Frame(self.right_tab_control,
                                width = self.canvasWidth + 10,
                                height = self.canvasHeight + 10)
        self.right_tab_control.add(self.right_frame,text="Maze")
        self.right_tab_control.add(self.right_frame_data,text="Data")
        
        self.right_tab_control.grid(row=0,column=1,padx=10,pady=10)
        
        self.left_frame = Frame(self.master, width = 25,
                                height = self.canvasHeight+10)
        self.left_frame.grid(row=0,column=0,padx=10,pady=10)
        
        #Widget Building
        
        ##Right Frame
        self.myCanvas = Canvas(self.right_frame, bg='#1a293b',
                               height = self.canvasHeight,
                               width = self.canvasWidth)
        
        
        ##Left Frame
        self.mazeDimH = Label(self.left_frame,text="Maze Height")
        self.entryMazeDimensionHeight = Entry(self.left_frame, width=15)
        
        self.mazeDimW = Label(self.left_frame,text='Maze Width')
        self.entryMazeDimensionWidth = Entry(self.left_frame, width=15)
        
        self.drawMaze = Button(self.left_frame, text="Draw Maze")
        self.drawMaze["command"] = self.draw_one_solution_maze
        
        self.placeSolution = Button(self.left_frame, text="Path Tree")
        self.placeSolution["command"] = self.place_solution
        
        self.treeCount = Label(self.left_frame, text = "Tree Count: 0")
        self.pathLength = Label(self.left_frame, text = "Path Length: 0")
        
        self.massData = Label(self.left_frame, text="Mass Data Amount")
        self.entryMazeMassAmount = Entry(self.left_frame, width = 15)
        self.massDataPlot = Button(self.left_frame, text="Plot Data")
        self.massDataPlot["command"] = self.plot_maze_data
        
        self.gridLines = Button(self.left_frame, text = 'Grid Lines')
        self.gridLines['command'] = self.draw_grid_lines
        
        self.treeCountLeft = Label(self.left_frame, text = "Left Trees:")
        self.treeCountRight = Label(self.left_frame,text = 'Right Trees:')
        #Widget Placement
        
        ##Right Frame
        self.myCanvas.grid(row=0,column=0,padx=5,pady=5)
        
        ##Left Frame
        self.mazeDimH.grid(row=0,column=0,sticky=N)
        self.entryMazeDimensionHeight.grid(row=1,column=0,sticky=N)
        
        self.mazeDimW.grid(row=2,column=0,sticky=N)
        self.entryMazeDimensionWidth.grid(row=3,column=0,sticky=N)
        
        self.drawMaze.grid(row=4, column=0,sticky=N)
        self.placeSolution.grid(row=5,column=0,sticky=N)
        
        self.treeCount.grid(row=6, column=0,sticky=N)
        self.pathLength.grid(row=7, column = 0, sticky = N)
        
        self.massData.grid(row=8,column=0,sticky=N)
        self.entryMazeMassAmount.grid(row=9,column=0,sticky=N)
        self.massDataPlot.grid(row=10,column=0,sticky=N)
        
        self.gridLines.grid(row=11,column=0)
        
        self.treeCountLeft.grid(row=12,column=0)
        self.treeCountRight.grid(row=13,column=0)
        
    def draw_maze_perimeter(self):
        correction = [1,1]
        height = int(self.entryMazeDimensionHeight.get())
        width = int(self.entryMazeDimensionWidth.get())
        if height > width:
            correction[0] = width/height
        if width > height:
            correction[1] = height/width
        dy = ((self.canvasHeight-(2*self.padding))/height)*correction[1]
        dx = ((self.canvasWidth-(2*self.padding))/width)*correction[0]
        line_1 = [self.padding+dx,self.padding,
                  self.padding+width*dx,self.padding,
                  self.padding+width*dx,self.padding+height*dy]
        line_2 = [self.padding,self.padding,
                  self.padding,self.padding+height*dy,
                  self.padding+width*dx-dx,self.padding+height*dy]
        self.myCanvas.create_line(line_1, fill='#5a5c5e',
                                  smooth = False,tags='mazeWall',width = 4)
        self.myCanvas.create_line(line_2, fill='#5a5c5e',
                                  smooth = False,tags='mazeWall', width =4)
        
    def draw_grid_lines(self):
        correction = [1,1]
        height = int(self.entryMazeDimensionHeight.get())
        width = int(self.entryMazeDimensionWidth.get())
        if height > width:
            correction[0] = width/height
        if width > height:
            correction[1] = height/width
        dy = ((self.canvasHeight-(2*self.padding))/height)*correction[1]
        dx = ((self.canvasWidth-(2*self.padding))/width)*correction[0]
        for horizontal in range(height):
            line = [self.padding,self.padding+dy*(horizontal+1),
                    self.padding+width*dx,self.padding+dy*(horizontal+1)]
            self.myCanvas.create_line(line,fill = '#355285',
                                      smooth = False, tags = 'gridLines',width = 0.5)
        for vertical in range(width):
            line = [self.padding+dx*(vertical+1),self.padding,
                    self.padding+dx*(vertical+1),self.padding+height*dy]
            self.myCanvas.create_line(line,fill='#355285',
                                      smooth=False,tags='gridLines', width = 0.5)
        
    
    def draw_one_solution_maze(self):
        self.myCanvas.delete('mazeWall')
        self.myCanvas.delete('solutionTree')
        self.myCanvas.delete('solutionTreeFinal')
        self.myCanvas.delete('gridLines')
        self.maze = Maze(self.entryMazeDimensionHeight.get(),
                         self.entryMazeDimensionWidth.get())
        self.draw_maze_perimeter()
        self.maze.randomize_maze()
        correction = [1,1]
        height = int(self.entryMazeDimensionHeight.get())
        width = int(self.entryMazeDimensionWidth.get())
        if height > width:
            correction[0] = width/height
        if width > height:
            correction[1] = height/width
        dy = ((self.canvasHeight-(2*self.padding))/height)*correction[1]
        dx = ((self.canvasWidth-(2*self.padding))/width)*correction[0]
        post_list = self.maze.numeric_maze_directions()
        coord = []
        i = 0
        j = 0
        for row in post_list:
            for wall in row:
                coord.append((j*dx)+self.padding+dx)
                coord.append((i*dy)+self.padding+dy)
                coord.append(coord[0]+(directions[wall][1]*dx))
                coord.append(coord[1]+-(directions[wall][2]*dy))
                self.myCanvas.create_line(coord, fill='gray',smooth = False,
                                          tags='mazeWall',width=1.5)
                coord = []
                j+=1
            i+=1
            j=0
        quick_path = self.maze.quickest_path
        self.treeCount.config(text="Tree Count:"+str(self.maze.tree_count[2]))
        self.treeCountLeft.config(text="Left Trees:"+str(self.maze.tree_count[0]))
        self.treeCountRight.config(text="Right Trees:"+str(self.maze.tree_count[1]))
        self.pathLength.config(text="Path Length:"+str(len(quick_path)))
            
    
    
    def place_point(self):
        self.myCanvas.delete('oval')
        self.myCanvas.create_oval([int(self.entryMazeDimensionWidth.get())-1,
                                   int(self.entryMazeDimensionHeight.get()),
                                   int(self.entryMazeDimensionWidth.get())+1,
                                   int(self.entryMazeDimensionHeight.get())],
                                  tags = 'oval')
        
    def place_solution(self):
        self.myCanvas.delete('solutionTree')
        self.myCanvas.delete('solutionTreeFinal')
        correction = [1,1]
        height = int(self.entryMazeDimensionHeight.get())
        width = int(self.entryMazeDimensionWidth.get())
        if height > width:
            correction[0] = width/height
        if width > height:
            correction[1] = height/width
        dy = ((self.canvasHeight-(2*self.padding))/height)*correction[1]
        dx = ((self.canvasWidth-(2*self.padding))/width)*correction[0]
        push = 0.15*dx
        for edge in self.maze.solution_tree:
            coord = []
            if edge[0][1] == edge[1][1]:
                coord.append((edge[0][1]*dx)+(self.padding)+dx/2.0)
                coord.append((edge[0][0]*dy)+(self.padding)+dy/2.0-push)
                coord.append((edge[1][1]*dx)+(self.padding)+dx/2.0)
                coord.append((edge[1][0]*dy)+(self.padding)+dy/2.0+push)
            if edge[0][0] == edge[1][0]:
                coord.append((edge[0][1]*dx)+(self.padding)+dx/2.0-push)
                coord.append((edge[0][0]*dy)+(self.padding)+dy/2.0)
                coord.append((edge[1][1]*dx)+(self.padding)+dx/2.0+push)
                coord.append((edge[1][0]*dy)+(self.padding)+dy/2.0)
            self.myCanvas.create_line(coord, fill='#152230',
                                      tags='solutionTree',
                                      width=0.3*dx, smooth=True)
            
        for edge in self.maze.quickest_path:
            coord = []
            coord.append((edge[0][1]*dx)+(self.padding)+dx/2.0)
            coord.append((edge[0][0]*dy)+(self.padding)+dy/2.0)
            coord.append((edge[1][1]*dx)+(self.padding)+dx/2.0)
            coord.append((edge[1][0]*dy)+(self.padding)+dy/2.0)
            self.myCanvas.create_line(coord, fill='orange',
                                      tags='solutionTreeFinal',width=0.5)
        
            
            
            
        
    def plot_maze_data(self):
        agg = Maze_Aggregate(self.maze.height,self.maze.width)
        maze_data = agg.mass_randomize_data(int(self.entryMazeMassAmount.get()))
        
        df = pd.DataFrame(maze_data)
        
        figure1 = plt.Figure(figsize=(5, 5), dpi=100)
        bar1 = FigureCanvasTkAgg(figure1, self.right_frame_data)
        bar1.get_tk_widget().grid(row=1,column=0)
        
        #TREE DATA UPPER
        ax1 = figure1.add_subplot(211)
        df.plot.scatter('left','right',ax=ax1)
        ax1.set_title("Trees to Solution Comparison")
        
        ax2 = figure1.add_subplot(212)
        df.plot.kde(ax=ax2)
        
        
        
        
        
        
        
        

root = Tk()
app = Application(master=root)
app.mainloop()
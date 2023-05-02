# -*- coding: utf-8 -*-
"""
Created on Mon May  1 17:28:57 2023

@author: Joshua.Mahurien
"""

directions = {0:('unassigned',(0,0),'black'),
              1:('left',(-1,0),'blue'),
              2:('up',(0,1),'green'),
              3:('right',(1,0),'yellow'),
              4:('down',(0,-1),'red')}

class Post:
    def __init__(self,direction,position):
        self.direction = direction
        self.position = position
        self.end_position = position
        
    def get_direction(self):
        return directions[self.direction][1]
    
    
    def change_end_position(self):
        self.end_position = self.position + self.get_direction()



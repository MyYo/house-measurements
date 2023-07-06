import numpy as np

def rotate_vec(vector, angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    rotated_vector = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ]).dot(vector)
    
    return rotated_vector
    
def distance(pt1,pt2):
    return ( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 )**0.5

class coordinate_convert:
    on_screen_origin = [] # On the screen where is 0,0 (u,v)
    x = [] # x direction (u,v), size is 1 inch
    y = [] # y direction (u,v), size is 1 inch
    def __init__(self, pt0, x, y):
        self.on_screen_origin = pt0
        self.x = x
        self.y = y
        
    def point_on_screen(self,pt): # Project x,y point (inches) to the screen pixels, returns a vector
        u = self.x[0]*pt[0]+self.y[0]*pt[1] + self.on_screen_origin[0]
        v = self.x[1]*pt[0]+self.y[1]*pt[1] + self.on_screen_origin[1]
        
        return np.transpose(np.array([u,v]))

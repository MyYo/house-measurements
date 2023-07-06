import tkinter as tk
import numpy as np
import time
from coordinate_convert import coordinate_convert
from coordinate_convert import rotate_vec
from coordinate_convert import distance

def setup_gui():
    global root
    global canvas
    global instructions_label
    
    # Create a tkinter window
    root = tk.Tk()
    root.geometry("800x600")  # Set window size
    root.attributes('-fullscreen', True) # Full screen

    # Create a canvas to draw lines
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()

    # Create a menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    # Create calibration menu
    calibrate_menu = tk.Menu(menu_bar)
    menu_bar.add_cascade(label="Calibrate", menu=calibrate_menu)
    calibrate_menu.add_command(label="Calibrate Point", command=calibrate)
    
    # Create draw menu
    draw_menu = tk.Menu(menu_bar)
    menu_bar.add_cascade(label="Draw", menu=draw_menu)
    draw_menu.add_command(label="Draw the Square", command=draw_square)
    draw_menu.add_command(label="Move the Saqare", command=move_square)
    draw_menu.add_command(label="Resize the Square", command=resize_square)
    
    menu_bar.add_command(label="Exit", command=exit_software)
    
    instructions_label = tk.Label(root, text="")
    instructions_label.place(x=1920/2, y=1080/2, anchor="center")

    # Start the tkinter event loop
    root.mainloop()

def on_do_nothing(event):
    return

# Function to handle calibration button click event
def calibrate():
    # Start calibration mode from scratch
    global calibrate_mode
    global instructions_label
    global canvas
    global root
    calibrate_mode = "Pick A Spot"
    instructions_label.config(text="Click on a spot to start calibration")

    #canvas.bind("<Button-1>", on_click_calibrate)
    root.bind("<KeyPress>", on_key_press_calibrate)

# Function to handle mouse click event in calibration mode
def on_click_calibrate(event):
    event_pt = np.transpose(np.array((event.x, event.y)))
    progress_on_calibrate(event_pt)
    
def on_key_press_calibrate(event):
    global line_op1, line_op2, line_op3
    global focus_pt
    
    if event.keysym == 'r':
        event_pt = line_op1
    elif event.keysym == 'g':
        event_pt = line_op2
    elif event.keysym == 'b':
        event_pt = line_op3
    else:
        return
    
    event_pt = event_pt + focus_pt
        
    progress_on_calibrate(event_pt)
    
def progress_on_calibrate(event_pt):
    global calibrate_mode
    global canvas, root
    global focus_pt
    global instructions_label
    global x # Define x direction in pixels along the horizontal (u) and vertical (v) screen axis
    global y # Define y direction in pixels along the horizontal (u) and vertical (v) screen axis
    global line_op1, line_op2, line_op3
    global scale
    global cc
    
    if calibrate_mode == "Pick A Spot":
        # Record focus point
        focus_pt = event_pt
        
        # Define deafult horizontal line units in pixels
        x = np.transpose(np.array([100,0]))
        calibrate_mode = "H Line Angle"
        line_op1 = x
        line_op2 = x
        line_op3 = x
        scale = 90.0
    
    if calibrate_mode == "H Line Angle":
        b=0
        
        # Figure out on what line the user clicked
        d1 = distance(focus_pt+line_op1-b,event_pt)
        d2 = distance(focus_pt+line_op2,event_pt)
        d3 = distance(focus_pt+line_op3+b,event_pt)
        
        if d1 < d2:
            x = line_op1
            scale = 0.9*scale
        elif d3 < d2:
            x = line_op3
            scale = 0.9*scale
        else:
            scale = 0.5*scale
            
        if scale < 5:
            # Angle is done, move to scale
            calibrate_mode = "H Line Size"
            scale = 1
            line_op1 = x
            line_op2 = x
            line_op3 = x
        else:
            # Set instructions
            line_op1 = rotate_vec(x, scale)*0.6
            line_op2 = x 
            line_op3 = rotate_vec(x, -scale)*1.4
        
            instructions_label.config(text="Use r,g,b to select the line closest to Horizontal (Red, Green, Blue)")
            
        
    if calibrate_mode == "H Line Size":
        b=10
        # Figure out on what line the user clicked
        d1 = distance(focus_pt+line_op1-b,event_pt)
        d2 = distance(focus_pt+line_op2,event_pt)
        d3 = distance(focus_pt+line_op3+b,event_pt)
        
        if d1 < d2:
            x = line_op1
            scale = 0.9*scale
        elif d3 < d2:
            x = line_op3
            scale = 0.9*scale
        else:
            scale = 0.5*scale
            
        if scale < 0.05:
            # size is done, move to V angle
            calibrate_mode = "V Line Angle"
            y = rotate_vec(x,90)
            line_op1 = y
            line_op2 = y
            line_op3 = y
            scale = 90
        else:
            # Set instructions
            line_op1 = x*(1-scale)
            line_op2 = x 
            line_op3 = x*(1+scale)
        
            instructions_label.config(text="Use r,g,b to select the line closest to 20 inches (Red, Green, Blue)")
    
    if calibrate_mode == "V Line Angle":
        b=0
        
        # Figure out on what line the user clicked
        d1 = distance(focus_pt+line_op1-b,event_pt)
        d2 = distance(focus_pt+line_op2,event_pt)
        d3 = distance(focus_pt+line_op3+b,event_pt)
        
        if d1 < d2:
            y = line_op1
            scale = 0.9*scale
        elif d3 < d2:
            y = line_op3
            scale = 0.9*scale
        else:
            scale = 0.5*scale
            
        if scale < 5:
            # Angle is done, move to scale
            calibrate_mode = "V Line Size"
            scale = 1
            line_op1 = y
            line_op2 = y
            line_op3 = y
        else:
            # Set instructions
            line_op1 = rotate_vec(y, scale)*0.6
            line_op2 = y 
            line_op3 = rotate_vec(y, -scale)*1.4
        
            instructions_label.config(text="Click on the end of the closest line to Vertical (Red, Geen or Blue), or use keys r,g,b")
            
    if calibrate_mode == "V Line Size":
        b=10
        # Figure out on what line the user clicked
        d1 = distance(focus_pt+line_op1-b,event_pt)
        d2 = distance(focus_pt+line_op2,event_pt)
        d3 = distance(focus_pt+line_op3+b,event_pt)
        
        if d1 < d2:
            y = line_op1
            scale = 0.9*scale
        elif d3 < d2:
            y = line_op3
            scale = 0.9*scale
        else:
            scale = 0.5*scale
            
        if scale < 0.05:
            # We are done
            calibrate_mode = "Done"
            instructions_label.config(text="Calibration Done")
            canvas.delete("all") # Clear the canvas from all lines
            canvas.bind("<Button-1>", on_do_nothing)
            root.bind("<KeyPress>", on_do_nothing)
            cc = coordinate_convert(focus_pt,x/10,y/10)
            
            return
            
        else:
            # Set instructions
            line_op1 = y*(1-scale)
            line_op2 = y 
            line_op3 = y*(1+scale)
        
            instructions_label.config(text="Click on the end of the closest line to 10 inches (Red, Geen or Blue),or use keys r,g,b")
    
    # Before we draw, clear canvas
    canvas.delete("all") # Clear the canvas from all lines
    
    # Draw focus point
    canvas.create_line(focus_pt[0]-10, focus_pt[1], focus_pt[0]+10, focus_pt[1], fill='black')
    canvas.create_line(focus_pt[0], focus_pt[1]-10, focus_pt[0], focus_pt[1]+10, fill='black')
    
    # Draw 3 options
    canvas.create_line(focus_pt[0]-b, focus_pt[1]-b, focus_pt[0]+line_op1[0]-b, focus_pt[1]+line_op1[1]-b, fill='red', width=4)
    canvas.create_line(focus_pt[0]   , focus_pt[1]   , focus_pt[0]+line_op2[0], focus_pt[1]+line_op2[1], fill='green', width=4)
    canvas.create_line(focus_pt[0]+b, focus_pt[1]+b, focus_pt[0]+line_op3[0]+b, focus_pt[1]+line_op3[1]+b, fill='blue', width=4)
    

class on_screen_square:
    def __init__(self, root, canvas, cc):
        self.square_center_in = np.transpose(np.array([0,0]))
        self.square_width_in = 20
        self.square_height_in = 10
        self.cc = cc
        self.canvas = canvas
        
        # Create aempty labels
        self.width_label = tk.Label(root, text="")
        self.width_label.place(x=400, y=300, anchor="center")
        self.height_label = tk.Label(root, text="")
        self.height_label.place(x=400, y=300, anchor="center")
        
    def draw_square(self):
        # Define the four corners of the square
        tl = np.copy(self.square_center_in)
        tl[0] = tl[0] - self.square_width_in/2
        tl[1] = tl[1] - self.square_height_in/2
        tr = np.copy(self.square_center_in)
        tr[0] = tr[0] + self.square_width_in/2
        tr[1] = tr[1] - self.square_height_in/2
        bl = np.copy(self.square_center_in)
        bl[0] = bl[0] - self.square_width_in/2
        bl[1] = bl[1] + self.square_height_in/2
        br = np.copy(self.square_center_in)
        br[0] = br[0] + self.square_width_in/2
        br[1] = br[1] + self.square_height_in/2
        
        # Convert corners to pixels space
        tl = self.cc.point_on_screen(tl)
        tr = self.cc.point_on_screen(tr)
        bl = self.cc.point_on_screen(bl)
        br = self.cc.point_on_screen(br)
        
        # Draw lines on screen
        self.canvas.delete("all") # Clear the canvas from all lines
        self.canvas.create_line(tl[0], tl[1], tr[0], tr[1], fill='red', width=4)
        self.canvas.create_line(tr[0], tr[1], br[0], br[1], fill='red', width=4)
        self.canvas.create_line(br[0], br[1], bl[0], bl[1], fill='red', width=4)
        self.canvas.create_line(bl[0], bl[1], tl[0], tl[1], fill='red', width=4)
        
        # Draw label on screen
        self.width_label.place(x=(tl[0]+tr[0])/2, y=tr[1]-12, anchor="center")
        self.width_label.config(text=f"{self.square_width_in} in")
        self.height_label.place(x=tr[0]+2, y=(tl[1]+bl[1])/2, anchor="w")
        self.height_label.config(text=f"{self.square_height_in} in")

    
def draw_square():
    global oss
    global cc
    global canvas
    global root
    oss = on_screen_square(root, canvas, cc)
    oss.draw_square()
    
def move_square():
    global root, instructions_label
    root.bind("<KeyPress>", on_key_press_move_square)
    instructions_label.config(text="Use asdw to move square around (1 inch)")

def on_key_press_move_square(event):
    global oss
    
    if event.keysym == 'a':
        oss.square_center_in[0] = oss.square_center_in[0] - 1
    elif event.keysym == 'd':
        oss.square_center_in[0] = oss.square_center_in[0] + 1
    elif event.keysym == 'w':
        oss.square_center_in[1] = oss.square_center_in[1] - 1
    elif event.keysym == 's':
        oss.square_center_in[1] = oss.square_center_in[1] + 1
    else:
        return
    
    oss.draw_square()
    
def resize_square():
    global root, instructions_label
    root.bind("<KeyPress>", on_key_press_resize_square)
    instructions_label.config(text="Use asdw to resize square (1 inch)")

def on_key_press_resize_square(event):
    global oss
    
    if event.keysym == 'a':
        oss.square_width_in = oss.square_width_in - 1
    elif event.keysym == 'd':
        oss.square_width_in = oss.square_width_in + 1
    elif event.keysym == 'w':
        oss.square_height_in = oss.square_height_in - 1
    elif event.keysym == 's':
        oss.square_height_in = oss.square_height_in + 1
    else:
        return
    
    oss.draw_square()
    
def exit_software():
    exit()

    
setup_gui()

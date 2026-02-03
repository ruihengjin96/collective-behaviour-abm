# Inspired by beneater's boid js code
""" v3 updates 
Modularization - separating the code into multiple files:
- Make hidden dependencies obvious (ongoing - go through every function and examine hidden dependencies, e.g., a lot of them depend on the global list boids)

Adding interactive widgets:
- Added sliders for avoid_dist (cohesion for boids) and flee_dist (boids fleeing from predators)

Debugging simulation window:
- Disabled resizing of window for now, as it was causing glitches. To be added at a later stage.

Allow boids to be eaten:
- Added a check is_eaten(boid, predators) that returns T or F, which is then looped over all boids, and only survivors are filtered at each timestep
- The rule for determining if a boid is eaten is very rudimentary right now, doesn't take into account the heading of the predator, and allows multiple boids to be eaten simultaneously

Delaying predator spawns:
- Added a button which releases predators, however, currently there is nothing preventing the button from being pressed multiple times

Changed spawning location for boids and predators:
- Boids spawn in a rectangle smaller than the arena, centered at the middle of the canvas. 
- Predators spawn at a corner of the arena, currently bottom right corner

Adding refuge:
- Added a circular refuge area, repelling predators when they enter a buffer zone around it

"""

import random
import math
import tkinter as tk
import numpy as np

# -------------------------------
# CONFIGURATION
# -------------------------------
## CANVAS CONFIGURATION
WIDTH = 800
HEIGHT = 600
MARGIN = 100

## BOID CONFIGURATION
NUM_BOIDS = 200
BOID_VIS_RANGE = 75
SPEED_LIMIT = 10
TURN_FACTOR = 3
BOID_CENTERING_FACTOR = 0.005
AVOID_FACTOR = 0.05
MATCHING_FACTOR = 0.05
DFLT_AVOID_DIST = 10
DRAW_TRAIL = False
DFLT_FLEE_DIST = 100
FLEE_FACTOR = 1.5

"""Trying to bind some variables to Tkinter widgets
added a live version of AVOID_DIST to within main()"""

## PREDATOR CONFIGURATION
NUM_PREDS = 10
HUNTING_SIGHT = 50
PRED_COHESION_VIS_RANGE = 100
PRED_CENTERING_FACTOR = 0.005
HEARING_RANGE = HUNTING_SIGHT*4
PRED_AVOID_RADIUS = 50
PRED_REP_HUNT_FACTOR = 0.2
PRED_REP_WANDER_FACTOR = 0.5
CATCH_DIST = 40 # make it big to test if it works

## REFUGE CONFIGURATION -- Defining it as a circular refuge first
REFUGE_R = 150
REFUGE_CX = 400
REFUGE_CY = 300
REFUGE_REPEL = 20
REFUGE_BUFFER = 50

class Circ_refuge:
    def __init__(self, x, y, r, repel, buff):
        self.x = x
        self.y = y
        self.r = r
        self.repel = repel # repel force
        self.buff = buff
        
cref = Circ_refuge(REFUGE_CX, REFUGE_CY, REFUGE_R, REFUGE_REPEL, REFUGE_BUFFER)

# -------------------------------
# CLASS DEFINITIONS
# -------------------------------
class Boid:
    def __init__(self, x, y, dx, dy, fov = 0.75*np.pi):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.fov = fov
        self.head = math.atan2(self.dy, self.dx)
        self.speed = math.hypot(self.dx, self.dy)
        self.max_turn = math.pi * 0.2
        self.max_turn_flee = math.pi * 0.3
        self.cohesion_visual_range = BOID_VIS_RANGE
        self.centering_factor = BOID_CENTERING_FACTOR
        self.history = []
        self.state = "calm"
        """Maybe could add a state variable (roaming/alert)"""

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def angle(self, other):
        theta = math.atan2(other.y-self.y, other.x-self.x)
        # might need a way to normalize the angles
        diff = self.head - theta
        norm_abs_diff = abs((diff+math.pi)%(2*math.pi)-math.pi)
        return norm_abs_diff 
    def draw(self, canvas): # Presumably need to pass a canvas argument into this method
        angle = math.atan2(self.dy, self.dx)
        x, y = self.x, self.y
        p1 = (x, y)
        p2 = (x - 15 * math.cos(angle) + 5 * math.sin(angle),
              y - 15 * math.sin(angle) - 5 * math.cos(angle))
        p3 = (x - 15 * math.cos(angle) - 5 * math.sin(angle),
              y - 15 * math.sin(angle) + 5 * math.cos(angle))
        canvas.create_polygon([p1, p2, p3], fill="#558cf4", outline="", tags = "agents")
        
# vectorized version
"""    def angle_to_others(self, others):
        heading = math.atan2(self.dy, self.dx)
        others_pos = np.array([[o.x, o.y] for o in others]) # shape = (N,2)
        
        #This is a list comprehension, make an array from a list of lists
        #more explicit version:
        #`positions = []
        #for o in others:
        #    positions.append([o.x, o.y])
        
        others_pos = np.array(positions)`
        my_pos = np.array([self.x, self.y])
        diff = my_pos - others_pos
        theta = np.arctan2(diff[:,1], diff[:,0])
        
        angle_diff = heading - theta
        norm_abs_angles = (angle_diff + np.pi)
        
        in_fov = np.abs(norm_abs_angles) <= (self.fov/2)
        return in_fov"""
    


class Predator(Boid):
    def __init__(self, x, y, dx, dy, fov = 0.5*np.pi):
        super().__init__(x, y, dx, dy, fov)
        self.move_state = "wander"
        self.signal_state = "off"
        self.signal_timer = 0
        self.signal_pos = []
        self.signal_response_strength = 0.02
        self.max_turn_wander = math.pi * 0.1
        self.max_turn = math.pi * 0.15
        self.repel_dist_wander = HUNTING_SIGHT
        self.repel_dist_hunt = HUNTING_SIGHT*2
        self.cohesion_visual_range = PRED_COHESION_VIS_RANGE
        self.centering_factor = PRED_CENTERING_FACTOR
        # wander speed multiplier
        # hunting speed multiplier
    def draw(self, canvas): # Presumably need to pass a canvas argument into this method
        angle = math.atan2(self.dy, self.dx)
        x, y = self.x, self.y
        p1 = (x, y)
        p2 = (x - 20 * math.cos(angle) + 7 * math.sin(angle),
              y - 20 * math.sin(angle) - 7 * math.cos(angle))
        p3 = (x - 20 * math.cos(angle) - 7 * math.sin(angle),
              y - 20 * math.sin(angle) + 7 * math.cos(angle))
        canvas.create_polygon([p1, p2, p3], fill="#d94b4b", outline="", tags = "agents")
        
        # draw signal halo if signal on
        if self.signal_timer > 0:
            radius = HUNTING_SIGHT
            alpha = int(255 * (self.signal_timer /10)) # fade out over 10 frames???
            canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                outline = "yellow", width = 2,
                tags = "agents"
            )        
            self.signal_timer -= 1

        


# -------------------------------
# INITIALIZATION
# -------------------------------
boids = []

def init_boids(canvas_width, canvas_height):
    for _ in range(NUM_BOIDS):
        boids.append(
            Boid(
                x=random.uniform(0.2*canvas_width, 0.8* canvas_width),  # generates a number between 0 and 1 and multiply by width
                y=random.uniform(0.2*canvas_height, 0.8* canvas_height),
                dx=random.uniform(-5, 5),  # initial dx, dy between -5 and 5
                dy=random.uniform(-5, 5),
            )
        )


preds = []

def init_predators(canvas_width, canvas_height):
    for _ in range(NUM_PREDS):
        preds.append(
            Predator(
                x=random.uniform(canvas_width*0.9, canvas_width),
                y=random.uniform(canvas_height*0.9, canvas_height),
                dx=random.uniform(-3, 3), # initial dx, dy between -3 and 3
                dy=random.uniform(-3, 3),
            )
        )
        
def init_predators_wrap():
    init_predators(WIDTH, HEIGHT)



# -------------------------------
# RULES
# -------------------------------

## BOID RULES
def detect_preds(boid, flee_dist):
    close_preds = [p for p in preds if boid.distance(p) < flee_dist]
    if close_preds:
        boid.state = "alarm"
    else:
        boid.state = "calm"     

def move_toward_center(agent, others): # used by both boids and predators
    center_x = 0
    center_y = 0
    num_neighbors = 0

    for other in others:
        if agent != other and agent.distance(other) < agent.cohesion_visual_range and agent.angle(other) <= agent.fov/2:
            center_x += other.x
            center_y += other.y
            num_neighbors += 1

    if num_neighbors:
        center_x /= num_neighbors
        center_y /= num_neighbors
        agent.dx += (center_x - agent.x) * agent.centering_factor
        agent.dy += (center_y - agent.y) * agent.centering_factor


def avoid_others(boid, avoid_dist):
    move_x = 0
    move_y = 0

    for other in boids:
        if boid != other and boid.distance(other) < avoid_dist:
            move_x += boid.x - other.x
            move_y += boid.y - other.y

    boid.dx += move_x * AVOID_FACTOR
    boid.dy += move_y * AVOID_FACTOR


def match_velocity(boid, neighbors):
    avg_dx = 0
    avg_dy = 0
    num_neighbors = 0

    for other in neighbors:
        if boid != other and boid.distance(other) < BOID_VIS_RANGE:
            avg_dx += other.dx
            avg_dy += other.dy
            num_neighbors += 1

    if num_neighbors:
        avg_dx /= num_neighbors
        avg_dy /= num_neighbors
        boid.dx += (avg_dx - boid.dx) * MATCHING_FACTOR
        boid.dy += (avg_dy - boid.dy) * MATCHING_FACTOR


def limit_speed(boid):
    speed = math.hypot(boid.dx, boid.dy)
    if speed > SPEED_LIMIT:
        scale = SPEED_LIMIT / speed
        boid.dx *= scale
        boid.dy *= scale


def keep_within_bounds(boid):
    if boid.x < MARGIN:
        boid.dx += TURN_FACTOR
    if boid.x > WIDTH - MARGIN:
        boid.dx -= TURN_FACTOR
    if boid.y < MARGIN:
        boid.dy += TURN_FACTOR
    if boid.y > HEIGHT - MARGIN:
        boid.dy -= TURN_FACTOR
        
def keep_away_refuge(boid, cref):
    dist_to_c = boid.distance(cref)
    if dist_to_c == 0:
        return
    
    dist_to_bound = dist_to_c - cref.r
    if dist_to_bound > cref.buff:
        return

    ux = (boid.x - cref.x) / dist_to_c
    uy = (boid.y - cref.y) / dist_to_c
    boid.dx += ux * cref.repel
    boid.dy += uy * cref.repel

            
    

def flee(boid, flee_dist):
    #find the predators that are within the flee zone
    close_preds = [p for p in preds if boid.distance(p) < flee_dist]
    if not close_preds:
        return
    #calculate their average position
    avg_x = sum(p.x for p in close_preds)/ len(close_preds)
    avg_y = sum(p.y for p in close_preds)/ len(close_preds)
    
    away_x = boid.x - avg_x
    away_y = boid.y - avg_y
    
    dist = math.hypot(away_x, away_y)
    if dist > 0:
        away_x /= dist
        away_y /= dist
    
    DESIRED_FLEE_SPEED = SPEED_LIMIT * 1.05
    desired_dx = away_x * DESIRED_FLEE_SPEED
    desired_dy = away_y * DESIRED_FLEE_SPEED
    
    STEER_ALPHA = 0.15
    boid.dx += (desired_dx - boid.dx) * STEER_ALPHA * FLEE_FACTOR
    boid.dy += (desired_dy - boid.dy) * STEER_ALPHA * FLEE_FACTOR

def is_eaten(boid, predators):
    for pred in predators:
        if boid.distance(pred) < CATCH_DIST:
            return True
    return False

## PREDATOR RULES

"""Rule 1: Stay at a distance from other predators"""
### write the following functions
def check_prey(pred):
    nearby_boids = [b for b in boids if pred.distance(b) <= HUNTING_SIGHT]
    """More explicit way:
    nearby_boids = []
    for boid in boids:
        if pred.distance(boid) <= HUNTING_SIGHT:
            nearby_boids.append(boid)
    """
    if nearby_boids:
        pred.signal_state = "on"
        pred.signal_timer = 10
        return True
    else:
        pred.signal_state = "off"
        return False
        

def check_signal(pred):
    signal_preds = [p for p in preds if p.signal_state == "on" and p != pred]
    if signal_preds:
        pred.signal_pos = (signal_preds[0].x, signal_preds[0].y)
        pred.signal_state = "on"
        return True
    else:
        pred.signal_pos = []
        return False

def wander(pred):
    delta_head = random.uniform(-pred.max_turn_wander, pred.max_turn_wander) 
    pred.head += delta_head
    pred.dx = pred.speed * math.cos(pred.head)
    pred.dy = pred.speed * math.sin(pred.head)

def pred_repel_check(pred):
    repel_wander = [p for p in preds if p != pred and pred.distance(p) < pred.repel_dist_wander]
    repel_hunt = [p for p in preds if p != pred and pred.distance(p) < pred.repel_dist_hunt]
    
    return [len(repel_wander)>0, len(repel_hunt)>0]

def pred_repel_wander(pred):
    nearby_other_preds = [p for p in preds if p != pred and pred.distance(p) < pred.repel_dist_wander]
    movex = 0
    movey = 0
    for other in nearby_other_preds:
        movex += pred.x - other.x
        movey += pred.y - other.y

    pred.dx += movex * PRED_REP_WANDER_FACTOR
    pred.dy += movey * PRED_REP_WANDER_FACTOR

def pred_repel_hunt(pred):
    nearby_other_preds = [p for p in preds if p != pred and pred.distance(p) < pred.repel_dist_hunt]
    movex = 0
    movey = 0
    for other in nearby_other_preds:
        movex += pred.x - other.x
        movey += pred.y - other.y

    pred.dx += movex * PRED_REP_HUNT_FACTOR
    pred.dy += movey * PRED_REP_HUNT_FACTOR
    
def move_toward_signal(pred):
    if not pred.signal_pos:
        return  # no signal to respond to
    
    target_x = pred.signal_pos[0]
    target_y = pred.signal_pos[1]
    # Compute vector toward signal
    dx = target_x - pred.x
    dy = target_y - pred.y

    # Optionally scale by a factor for smooth movement toward signal
    pred.dx += dx * pred.signal_response_strength
    pred.dy += dy * pred.signal_response_strength

    # Update heading and speed if needed
    pred.head = math.atan2(pred.dy, pred.dx)
    pred.speed = math.hypot(pred.dx, pred.dy)






"""Rule 2: Move toward the centroid of boids within hunting sight"""
def hunt(pred):
    # 1. Find all boids within the hunting sight
    close_boids = [b for b in boids if pred.distance(b) < HUNTING_SIGHT]
    if not close_boids:
        return
    
    # 2. Find the centroid of the boids
    avg_x = sum(b.x for b in close_boids) / len(close_boids)        
    avg_y = sum(b.y for b in close_boids) / len(close_boids)
    
    # 3. Compute the difference b/n boid position and predator position
    move_x = avg_x - pred.x
    move_y = avg_y - pred.y
    
    # 4. Predator move toward nearest boid
    pred.dx += move_x * 0.02 
    pred.dy += move_y * 0.02
    """Note: should parameterize this factor"""
    
    
"""Don't worry about drawing trails for now, add it later"""
#    if DRAW_TRAIL and len(boid.history) > 1:
#        canvas.create_line(boid.history, fill="#558cf466")


# -------------------------------
# ANIMATION
# -------------------------------
def update(canvas, avoid_dist_var, flee_dist_var):
    global boids
    canvas.delete("agents")

    avoid_dist = avoid_dist_var.get()
    flee_dist = flee_dist_var.get()
    
    # decide which boids are eaten
    eaten_boids = []
    for boid in boids:
        if is_eaten(boid, preds):
            eaten_boids.append(boid)
            
    # update list of boids to only include survivors
    boids = [b for b in boids if b not in eaten_boids]       
    
    # boid rules
    for boid in boids:
        detect_preds(boid, flee_dist)
        if boid.state == "alarm":
            flee(boid, flee_dist)
        else:
            move_toward_center(boid, boids)
            avoid_others(boid, avoid_dist)
            match_velocity(boid, boids)
            #keep_within_bounds(boid)
        limit_speed(boid)
        
        boid.x = (boid.x + boid.dx) % WIDTH
        boid.y = (boid.y + boid.dy) % HEIGHT

        boid.history.append((boid.x, boid.y))

        boid.history = boid.history[-50:]

        boid.draw(canvas)
    
    # predator rules    
    for pred in preds:
        pred.signal_state = "off"
        
        keep_away_refuge(pred, cref)

        prey_detected = check_prey(pred)
        signal_detected = check_signal(pred)
        pred_avoid = pred_repel_check(pred)

        if prey_detected: # hunt and send signal
            pred.signal_state = "on"
            hunt(pred)
            if pred_avoid[1]:
                pred_repel_hunt(pred)
            else:
                move_toward_center(pred, preds) 
        elif signal_detected: # follow signal and send signal
            pred.signal_state = "on"
            if pred_avoid[1]:
                pred_repel_hunt(pred)
            else:
                move_toward_signal(pred) 
        else: # wander and don't send signal
            pred.signal_state = "off"
            if pred_avoid[0]: # write a checking function for this
                pred_repel_wander(pred)
            else:
                wander(pred)
        limit_speed(pred)
        #keep_within_bounds(pred)
        pred.x = (pred.x + pred.dx) % WIDTH
        pred.y = (pred.y + pred.dy) % HEIGHT
        
        pred.history.append((pred.x, pred.y))
        pred.history = pred.history[-50:]
        pred.draw(canvas)        

    canvas.after(33, update, canvas, avoid_dist_var, flee_dist_var)  # ~30 FPS


# -------------------------------
# MAIN
# -------------------------------
def main():
    global WIDTH, HEIGHT

    root = tk.Tk()

    root.title("Boids Simulation")
    
    # Adding slider for AVOID_DIST
    control = tk.Frame(root)
    control.pack(side = tk.RIGHT, fill = tk.Y)

    # Creating arena
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    
    canvas.create_oval(
        REFUGE_CX - REFUGE_R, 
        REFUGE_CY - REFUGE_R, 
        REFUGE_CX + REFUGE_R, 
        REFUGE_CY + REFUGE_R
    )

    # Avoid_dist slider
    avoid_dist_var = tk.DoubleVar(value = DFLT_AVOID_DIST)
    tk.Label(control, text = "Boid avoid distance").pack()
    tk.Scale(
        control,
        from_=5,
        to=100,
        resolution = 1,
        orient = tk.HORIZONTAL,
        variable = avoid_dist_var
    ).pack()
    
    # Flee_dist slider
        # Flee distance slider
    flee_dist_var = tk.DoubleVar(value=DFLT_FLEE_DIST)
    tk.Label(control, text="Boid flee distance").pack()
    tk.Scale(
        control,
        from_=50,
        to=300,
        resolution=5,
        orient=tk.HORIZONTAL,
        variable=flee_dist_var
    ).pack()
    
    # Release predator button
    tk.Button(
        control, 
        text = "Release predators", 
        command = init_predators_wrap, 
    ).pack() # adding a button linked to callback function init_predators()

    
    canvas.update_idletasks()

    init_boids(WIDTH, HEIGHT)  
    #canvas.after(5000, init_predators, WIDTH, HEIGHT) # delay the spawning of predators by the specified amount of time in ms

    print(f"Initialized {len(preds)} predators")

    update(canvas, avoid_dist_var, flee_dist_var)
    root.mainloop()


if __name__ == "__main__":
    main()
    

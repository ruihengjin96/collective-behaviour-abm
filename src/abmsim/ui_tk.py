# boidsim/ui_tk.py
import tkinter as tk
import math
from abmsim.model import Model
from abmsim.config import WIDTH, HEIGHT, DFLT_AVOID_DIST, DFLT_FLEE_DIST, REFUGE_R, REFUGE_CX, REFUGE_CY


def run():
    model = Model()
    model.init_boids()
    # model.init_predators() # commented out so as to not release predators until button is pressed

    root = tk.Tk()
    root.title("Boids Simulation (working title)")
    
    # Creating a Tkinter Frame -- aka a container for widgets
    ctrlpnl = tk.Frame(root) # ctrlpnl aka control panel
    ctrlpnl.pack(side = tk.RIGHT, fill = tk.Y)
    
    # Creating arena
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()
    
    # Drawing the circular refuge area
    canvas.create_oval(
          REFUGE_CX - REFUGE_R,
          REFUGE_CY - REFUGE_R, 
          REFUGE_CX + REFUGE_R, 
          REFUGE_CY + REFUGE_R,
          outline = "white", fill = "#e6f5f4", tags = "refuge"          
    )
    
    # Creating a slider for the distance threshold for repulsion between boids
    avoid_var = tk.DoubleVar(value=DFLT_AVOID_DIST)
    tk.Label(ctrlpnl, text = "Boid avoid distance").pack()
    tk.Scale(
        ctrlpnl,
        from_=5,
        to=100,
        resolution = 1,
        orient = tk.HORIZONTAL,
        variable = avoid_var
    ).pack()  
      
    # Creating a slider for the distance threshold at which boids start fleeing from predators
    flee_var = tk.DoubleVar(value=DFLT_FLEE_DIST)
    tk.Label(ctrlpnl, text = "Boid flee distance").pack()
    tk.Scale(
        ctrlpnl,
        from_=50,
        to=300,
        resolution = 5,
        orient = tk.HORIZONTAL,
        variable = flee_var
    ).pack() 
    
    # Creating a button that releases predators
    tk.Button(
          ctrlpnl,
          text = "Release predators",
          command = model.init_predators,
    ).pack()
    
    def draw():
        canvas.delete("agents")
        for b in model.boids:
            angle = math.atan2(b.dy, b.dx)
            x, y = b.x, b.y,
            p1 = (x, y)
            p2 = (x - 15 * math.cos(angle) + 5 * math.sin(angle),
                  y - 15 * math.sin(angle) - 5 * math.cos(angle))
            p3 = (x - 15 * math.cos(angle) - 5 * math.sin(angle),
                  y - 15 * math.sin(angle) + 5 * math.cos(angle))
            canvas.create_polygon([p1, p2, p3], fill="#56b1fc", outline="", tags = "agents")   
        for p in model.predators:
            angle = math.atan2(p.dy, p.dx)
            x, y = p.x, p.y,
            p1 = (x, y)
            p2 = (x - 20 * math.cos(angle) + 7 * math.sin(angle),
                  y - 20 * math.sin(angle) - 7 * math.cos(angle))
            p3 = (x - 20 * math.cos(angle) - 7 * math.sin(angle),
                  y - 20 * math.sin(angle) + 7 * math.cos(angle))
            canvas.create_polygon([p1, p2, p3], fill="#fc6056", outline="", tags = "agents")

    def loop():
        model.step(avoid_var.get(), flee_var.get())
        draw()
        canvas.after(33, loop)

    loop()
    root.mainloop()

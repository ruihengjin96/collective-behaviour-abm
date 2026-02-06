# boidsim/ui_tk.py
import tkinter as tk
import math
from abmsim.model import Model
from abmsim.config import WIDTH, HEIGHT, DFLT_AVOID_DIST, DFLT_FLEE_DIST


def run():
    model = Model()
    model.init_boids()
    model.init_predators()

    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    avoid_var = tk.DoubleVar(value=DFLT_AVOID_DIST)    
    flee_var = tk.DoubleVar(value=DFLT_FLEE_DIST)

    def draw():
        canvas.delete("all")
        for b in model.boids:
            angle = math.atan2(b.dy, b.dx)
            x, y = b.x, b.y,
            p1 = (x, y)
            p2 = (x - 15 * math.cos(angle) + 5 * math.sin(angle),
                  y - 15 * math.sin(angle) - 5 * math.cos(angle))
            p3 = (x - 15 * math.cos(angle) - 5 * math.sin(angle),
                  y - 15 * math.sin(angle) + 5 * math.cos(angle))
            canvas.create_polygon([p1, p2, p3], fill="#558cf4", outline="", tags = "agents")   
        for p in model.predators:
            angle = math.atan2(p.dy, p.dx)
            x, y = p.x, p.y,
            p1 = (x, y)
            p2 = (x - 20 * math.cos(angle) + 7 * math.sin(angle),
                  y - 20 * math.sin(angle) - 7 * math.cos(angle))
            p3 = (x - 20 * math.cos(angle) - 7 * math.sin(angle),
                  y - 20 * math.sin(angle) + 7 * math.cos(angle))
            canvas.create_polygon([p1, p2, p3], fill="#d94b4b", outline="", tags = "agents")

    def loop():
        model.step(avoid_var.get(), flee_var.get())
        draw()
        canvas.after(33, loop)

    loop()
    root.mainloop()

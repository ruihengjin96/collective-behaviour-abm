# boidsim/ui_tk.py
import tkinter as tk
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
            canvas.create_oval(b.x-3, b.y-3, b.x+3, b.y+3, fill="blue")
        for p in model.predators:
            canvas.create_oval(p.x-5, p.y-5, p.x+5, p.y+5, fill="red")

    def loop():
        model.step(avoid_var.get(), flee_var.get())
        draw()
        canvas.after(33, loop)

    loop()
    root.mainloop()

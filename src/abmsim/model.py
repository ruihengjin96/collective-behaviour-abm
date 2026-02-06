# abmsim/model.py
import random
from abmsim.agents import Boid, Predator
from abmsim.config import NUM_BOIDS, NUM_PREDS, WIDTH, HEIGHT, DFLT_AVOID_DIST
from abmsim.rules.boid_rules import (
    avoid_others, match_velocity, is_eaten, detect_preds, flee
)
from abmsim.rules.predator_rules import (hunt, check_prey, check_signal, pred_repel_check, pred_repel_hunt, move_toward_signal, pred_repel_wander, wander)
from abmsim.rules.shared_rules import (limit_speed, move_toward_center)


class Model:
    def __init__(self):
        self.boids = []
        self.predators = []

    def init_boids(self):
        for _ in range(NUM_BOIDS):
            self.boids.append(
                Boid(
                    random.uniform(100, WIDTH - 100),
                    random.uniform(100, HEIGHT - 100),
                    random.uniform(-5, 5),
                    random.uniform(-5, 5),
                )
            )

    def init_predators(self):
        for _ in range(NUM_PREDS):
            self.predators.append(
                Predator(
                    random.uniform(0, WIDTH),
                    random.uniform(0, HEIGHT),
                    random.uniform(-3, 3),
                    random.uniform(-3, 3),
                )
            )

    def step(self, avoid_dist, flee_dist):
        # remove eaten boids
        eaten_boids = []
        for b in self.boids:
            if is_eaten(b, self.predators):
                eaten_boids.append(b)
        self.boids = [b for b in self.boids if b not in eaten_boids]
        
        # boid interaction rules
        for b in self.boids:
            avoid_others(b, self.boids, avoid_dist)
            match_velocity(b, self.boids)
            limit_speed(b)
            b.x = (b.x + b.dx) % WIDTH
            b.y = (b.y + b.dy) % HEIGHT

        # predator interaction rules
        for p in self.predators:
            hunt(p, self.boids)
            limit_speed(p)
            p.x = (p.x + p.dx) % WIDTH
            p.y = (p.y + p.dy) % HEIGHT

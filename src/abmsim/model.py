# abmsim/model.py
import random
from abmsim.agents import Boid, Predator
from abmsim.config import NUM_BOIDS, NUM_PREDS, WIDTH, HEIGHT, DFLT_AVOID_DIST
from abmsim.rules.boid_rules import (
    avoid_others, match_velocity, is_eaten
)
from abmsim.rules.predator_rules import hunt
from abmsim.rules.shared_rules import limit_speed


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
        self.boids = [
            b for b in self.boids if not is_eaten(b, self.predators)
        ]
        
        # boids
        for b in self.boids:
            avoid_others(b, self.boids, avoid_dist)
            match_velocity(b, self.boids)
            limit_speed(b)
            b.x = (b.x + b.dx) % WIDTH
            b.y = (b.y + b.dy) % HEIGHT

        # predators
        for p in self.predators:
            hunt(p, self.boids)
            limit_speed(p)
            p.x = (p.x + p.dx) % WIDTH
            p.y = (p.y + p.dy) % HEIGHT

# abmsim/model.py
import random
from abmsim.agents import Boid, Predator
import abmsim.config as config
from abmsim.rules.boid_rules import (
    avoid_others, match_velocity, is_eaten, detect_preds, flee
)
from abmsim.rules.predator_rules import (hunt, check_prey, check_signal, pred_repel_check, pred_repel_hunt, move_toward_signal, pred_repel_wander, wander, keep_away_refuge)
from abmsim.rules.shared_rules import (limit_speed, move_toward_center)
from abmsim.environment import cref


class Model:
    def __init__(self):
        self.boids = []
        self.predators = []

    def init_agents(self, agent_type, n):
        agent_config = {
            'Boid': {
                'class': Boid,
                'list': self.boids,
                'x_bounds': (100, config.WIDTH - 100),
                'y_bounds': (100, config.HEIGHT - 100),
                'dx_bounds': (-5, 5),
                'dy_bounds': (-5, 5),
            },
            'Predator': {
                'class': Predator,
                'list': self.predators,
                'x_bounds': (0, config.WIDTH),
                'y_bounds': (0, config.HEIGHT),
                'dx_bounds': (-3, 3),
                'dy_bounds': (-3, 3),
            }
        }
        if agent_type not in agent_config:
            raise ValueError(f"Unknown agent type: {agent_type}.")
        cfg = agent_config[agent_type]
        for _ in range(n):
            cfg['list'].append(
                cfg['class'](
                    random.uniform(cfg['x_bounds'][0], cfg['x_bounds'][1]),
                    random.uniform(cfg['y_bounds'][0], cfg['y_bounds'][1]),
                    random.uniform(cfg['dx_bounds'][0], cfg['dx_bounds'][1]),
                    random.uniform(cfg['dy_bounds'][0], cfg['dy_bounds'][1])
                )
            )

    def step(self, avoid_dist, flee_dist, catch_dist, speedlim):
        # remove eaten boids
        eaten_boids = []
        for b in self.boids:
            if is_eaten(b, self.predators, catch_dist):
                eaten_boids.append(b)
        self.boids = [b for b in self.boids if b not in eaten_boids]
        
        # boid interaction rules
        for b in self.boids:
            detect_preds(b, self.predators, flee_dist)
            if b.state == "alarm":
                flee(b, self.predators, flee_dist)
            else:
                move_toward_center(b, self.boids)
                avoid_others(b, self.boids, avoid_dist)
                match_velocity(b, self.boids)
            limit_speed(b, speedlim)
            b.x = (b.x + b.dx) % config.WIDTH
            b.y = (b.y + b.dy) % config.HEIGHT

        # predator interaction rules
        for p in self.predators:
            p.signal_state = "off"
            
            prey_detected = check_prey(p, self.boids)
            signal_detected = check_signal(p, self.predators)
            pred_avoid = pred_repel_check(p, self.predators)
            #keep_away_refuge(p, cref)
            if prey_detected:
                p.signal_state = "on"
                hunt(p, self.boids)
                if pred_avoid[1]:
                    pred_repel_hunt(p, self.predators)
                else:
                    move_toward_center(p, self.predators)
            elif signal_detected:
                p.signal_state = "on"
                if pred_avoid[1]:
                    pred_repel_hunt(p, self.predators)
                else:
                    move_toward_signal(p)
            else:
                p.signal_state = "off"
                if pred_avoid[0]:
                    pred_repel_wander(p, self.predators)
                else:
                    wander(p)
            limit_speed(p, speedlim)
            p.x = (p.x + p.dx) % config.WIDTH
            p.y = (p.y + p.dy) % config.HEIGHT
    
    def clear(self):
        self.boids.clear()
        self.predators.clear()
#test connectivity

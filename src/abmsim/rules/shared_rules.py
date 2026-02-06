# -------------------------------
# SHARED RULES
# -------------------------------
import math
from abmsim.config import TURN_FACTOR, MARGIN, WIDTH, HEIGHT, SPEED_LIMIT

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

def limit_speed(boid):
    speed = math.hypot(boid.dx, boid.dy)
    if speed > SPEED_LIMIT:
        scale = SPEED_LIMIT / speed
        boid.dx *= scale
        boid.dy *= scale

def keep_within_bounds(boid): # I don't think it's currently used
    if boid.x < MARGIN:
        boid.dx += TURN_FACTOR
    if boid.x > WIDTH - MARGIN:
        boid.dx -= TURN_FACTOR
    if boid.y < MARGIN:
        boid.dy += TURN_FACTOR
    if boid.y > HEIGHT - MARGIN:
        boid.dy -= TURN_FACTOR


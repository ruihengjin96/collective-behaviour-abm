# -------------------------------
# BOID RULES
# -------------------------------
import math
from abmsim.config import SPEED_LIMIT, FLEE_FACTOR, AVOID_FACTOR, BOID_VIS_RANGE, MATCHING_FACTOR, CATCH_DIST

def detect_preds(boid, flee_dist):
    close_preds = [p for p in preds if boid.distance(p) < flee_dist]
    if close_preds:
        boid.state = "alarm"
    else:
        boid.state = "calm"     

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

def avoid_others(boid, boids, avoid_dist):
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

def is_eaten(boid, predators):
    for pred in predators:
        if boid.distance(pred) < CATCH_DIST:
            return True
    return False

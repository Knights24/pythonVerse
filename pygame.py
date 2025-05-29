import pygame
import math
import sys

# --- Constants ---
WIDTH, HEIGHT = 800, 800
BALL_RADIUS = 15
HEXAGON_RADIUS = 200
GRAVITY_STRENGTH = 0.3
ROTATION_SPEED = 0.01  # Radians per frame

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Inside Rotating Hexagon")
clock = pygame.time.Clock()
center = (WIDTH // 2, HEIGHT // 2)

# --- Utility Functions ---
def get_hexagon_points(center, radius, rotation):
    """Return the 6 rotated vertices of a regular hexagon"""
    points = []
    for i in range(6):
        angle = math.radians(60 * i) + rotation
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points

# --- Ball Class ---
class Ball:
    def __init__(self, radius, position, velocity=(0, 0)):
        self.radius = radius
        self.x, self.y = position
        self.vx, self.vy = velocity
        self.bounce = 0.8

    def apply_gravity(self, gravity_vector):
        self.vx += gravity_vector[0]
        self.vy += gravity_vector[1]

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

    def reflect_from_edge(self, p1, p2):
        """Reflects ball if it crosses a hexagon edge"""
        # Edge vector
        ex, ey = p2[0] - p1[0], p2[1] - p1[1]
        length = math.hypot(ex, ey)
        if length == 0:
            return

        # Normal vector (pointing inward)
        nx, ny = ey / length, -ex / length

        # Ball position relative to edge
        dx, dy = self.x - p1[0], self.y - p1[1]
        dist = dx * nx + dy * ny

        if dist > self.radius:
            # Push inside
            overlap = dist - self.radius
            self.x -= nx * overlap
            self.y -= ny * overlap

            # Reflect velocity
            dot = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot * nx
            self.vy -= 2 * dot * ny

            # Damping
            self.vx *= self.bounce
            self.vy *= self.bounce

# --- Simulation Setup ---
ball = Ball(BALL_RADIUS, (center[0], center[1] - 100))
hex_rotation = 0

# --- Main Loop ---
running = True
while running:
    screen.fill((20, 20, 20))
    dt = clock.tick(60) / 1000  # Time per frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update Hexagon ---
    hex_rotation += ROTATION_SPEED
    hex_points = get_hexagon_points(center, HEXAGON_RADIUS, hex_rotation)

    # --- Apply Rotating Gravity ---
    gx = -math.sin(hex_rotation) * GRAVITY_STRENGTH
    gy = math.cos(hex_rotation) * GRAVITY_STRENGTH
    ball.apply_gravity((gx, gy))
    ball.update_position()

    # --- Handle Collisions with Hexagon Edges ---
    for i in range(6):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % 6]
        ball.reflect_from_edge(p1, p2)

    # --- Draw Everything ---
    pygame.draw.polygon(screen, (255, 255, 255), hex_points, 2)
    pygame.draw.circle(screen, (255, 0, 0), (int(ball.x), int(ball.y)), ball.radius)

    pygame.display.flip()

# --- Cleanup ---
pygame.quit()
sys.exit()

import numpy as np

# Define the size of the hexagon
hex_size = 10.0

# Define the mass of the ball
mass = 0.1

# Define the gravity acting on the ball
gravity = -9.8  # m/s^2 (default: 9.8 N/kg)

# Define the time step for simulations
dt = 0.01

# Initialize the position and velocity of the ball
x = np.zeros(3)
v = np.zeros((3,))

# Generate a random starting position for the ball within the hexagon
x[0] = np.random.uniform(0, hex_size) - hex_size/2
x[1] = np.random.uniform(0, hex_size) - hex_size/2
x[2] = np.random.uniform(0, hex_size) - hex_size/2
v[0] = np.zeros(3)
v[1] = np.zeros(3)
v[2] = np.zeros(3)

# Define a function to update the position and velocity of the ball based on gravity and friction
def update_ball(x, v, dt):
    # Calculate the acceleration due to gravity
    a = -gravity * mass / np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
    
    # Calculate the frictional force acting on the ball
    f = 0.5 * (x[0] + x[1]) * 0.1 * dt
    
    # Update the position and velocity of the ball using the equations of motion
    x_new = x + v * dt + 0.5 * a * dt**2
    v_new = v - f * dt
    
    return x_new, v_new

# Simulate the motion of the ball for a fixed time step
for i in range(1000):
    x, v = update_ball(x, v, dt)

# Print the final position and velocity of the ball
print("Final position:", x)
print("Final velocity:", v)

def approach(speed1, speed2): # Calculates the speed of approach of the particles
    return abs(speed1 - speed2)

# Takes the initial self.velocities and self.masses of the particles, and the
# elasticity between them, and returns the final self.velocities of the two particles.
def collisionCalculator(speed1, speed2 , mass1, mass2, elasticity):
    speedofapproach = approach(speed1, speed2)
    # Simultaneous equations rearranged to calculate the velocity of the particle on the right
    v2 = (elasticity * (speedofapproach) + speed1 + (mass2 * speed2 / mass1)) / ((mass2 / mass1) + 1)
    # Value of v2 substituted to find the velocity of the particle on the left
    v1 = v2 - elasticity * (speedofapproach)
    return (v1, v2)

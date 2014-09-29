# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# PyParticles.py
#   Obtained from http://www.petercollingridge.co.uk/pygame-physics-simulation
#   License unknown
#   Provides physics (movements/collision) for the bubble sprites.
#   Slightly modified to integrate with Bubble Math. All modifications are
#   marked with a [Bubble Math] comment
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import math
import random

import gameflow     # [Bubble Math]

def addVectors((angle1, length1), (angle2, length2)):
    """ Returns the sum of two vectors """

    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle  = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)

def collide(p1, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce
        i.e. update their angle, speed and position

		[Bubble Math] This function now returns true
		or false to indicate if a collision occurred """

	# [Bubble Math] Bugfix
    if p1.speed > p2.speed:
        pTmp = p1
        p1 = p2
        p2 = pTmp

    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap
        return True
    else: # no collision
        return False

class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, (x, y), size=10, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9

    def move(self):
        """ Update position based on speed, angle
            Update speed based on drag """

        #(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

        # [Bubble Math] Prevent bubbles from moving infinitely
        if( self.speed < gameflow.MIN_SPEED ):
			self.speed = 0

    def mouseMove(self, x, y):
        """ Change angle and speed to move towards a given point """

        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

class Environment:
    """ Defines the boundary of a simulation and its properties """

    def __init__(self, (width, height)):
        self.width = width
        self.height = height
        self.particles = []

        self.colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = None

    def addParticles(self, n=1, **kargs):
        """ Add n particles with properties given by keyword arguments """

        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            particle = Particle((x, y), size, mass)
            particle.speed = kargs.get('speed', random.random())
            particle.angle = kargs.get('angle', random.uniform(0, math.pi*2))
            particle.colour = kargs.get('colour', (0, 0, 255))
            particle.drag = (particle.mass/(particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)

	# [Bubble Math] Used instead of addParticles()
    def addBubbles(self, bubbles):
        for bub in bubbles:
            self.particles.append(bub)
        return len(self.particles)

	# [Bubble Math] For removing bubbles from environment
    def delBubbles(self, bubbles):
        for bub in bubbles:
            self.particles.remove(bub)
        return len(self.particles)

    def update(self):
        """  Moves particles and tests for collisions with the walls and each other
		[Bubble Math] This method now returns a list of collisions """

        collisions = []

        for i, particle in enumerate(self.particles):
            particle.move()
            if self.acceleration:
                particle.accelerate(self.acceleration)
            if self.bounce(particle):
                collisions.append( (None, None) )
            for particle2 in self.particles[i+1:]:
                if collide(particle, particle2):
                    collisions.append( (particle, particle2) )

        return collisions

    def bounce(self, particle):
        """ Tests whether a particle has hit the boundary of the environment """

        # [Bubble Math] Returning true if bounced
        bounced = False

        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity
            bounced = True

        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity
            bounced = True

        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity
            bounced = True

        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity
            bounced = True

        return bounced

    def findParticle(self, x, y):
        """ Returns any particle that occupies position x, y """

        for particle in self.particles:
            if math.hypot(particle.x - x, particle.y - y) <= particle.size:
                return particle
        return None

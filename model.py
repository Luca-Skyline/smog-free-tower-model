import math
import random

# for all particles
y0 = 2.4 # initial height, meters (also height of chamber)
l = 1.75 # width of chamber, meters
v_air = -2.26 # make a negative number
voltage = 1500 # voltage between plates, volts
rho_a = 1.225 # air denisty (kg / m^3)
rho_p = 600 # particle density (kg / m^3)
vi = 1.39e-5 # air kinematic viscosity 
g = 9.81 # acceleration of gravity, m / s^2
q = 1.6e-19 # charge of particle, Coulombs
A = 1.23 # cross-sectional area of chamber in m^2

dt = 0.001 # time step


def simulateParticle(particle):
    particle.posX
    particle.velX
    particle.mass
    particle.diameter
    
    # initial values
    t = 0
    
    while(particle.posX > 0 and particle.posX < l and particle.posY > 0):
        # force of buoyancy    
        Ff = (1/6) * math.pi * (rho_a) * g * (particle.diameter ** 3)
        
        # relative velocity (particle vs air)
        urx = particle.velX
        ury = particle.velY - v_air
        
        # force of form drag   
        Fdx = -3 * vi * rho_a * math.pi * particle.diameter * urx
        Fdy = -3 * vi * rho_a * math.pi * particle.diameter * ury
        
        # force of electric field from plate
        E = q * voltage / l
        
        # force of gravity
        W = -1 * particle.mass * g
        
        # instantaneous acceleration from Newton's second law
        ax = (Fdx + E) / particle.mass
        ay = (Fdy + Ff + W) / particle.mass
        
        # apply Euler's method to velocity and position
        particle.velX += ax * dt
        particle.velY += ay * dt
        particle.posX += particle.velX * dt
        particle.posY += particle.velY * dt
        
        # increment time  
        t += dt
        
    if(particle.posX <= 0 or particle.posY >= l):
        return 1
    return 0

class Particle:
    def __init__(self, posX, posY, velX, velY, diameter, mass):
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.mass = mass
        self.diameter = diameter

def generateParticles(totParticles):

    listOfParticles = []
    numPm25 = int(totParticles * (14 + 19) / (14 + 19 + 24 + 29)) #ratio of pm2.5 particles
    numPm10 = int(totParticles * (24 + 29) / (14 + 19 + 24 + 29)) # ratio of pm10 particles

    # generate pm2.5 particles
    for i in range(0, numPm25):
        p = generateSingleParticle(0, 2.5 * pow(10, -6))
        listOfParticles.append(p)
         
    # generate pm 10 particles
    for i in range(0, numPm10):
        p = generateSingleParticle(2.5 * pow(10, -6), 10.0 * pow(10, -6))
        listOfParticles.append(p)

    return listOfParticles

def generateSingleParticle(diamMin, diamMax):
    diameter = random.uniform(diamMin, diamMax)
    posX = random.uniform(0, l)
    mass = 1 / 6 * math.pi * rho_p * pow(diameter, 3)
    p = Particle(posX, y0, 0, v_air, diameter, mass)
    return p

ps = generateParticles(10)

for p in ps:
    simulateParticle(p)
    print(f" {p.posX:.2f} - {p.diameter} - {p.mass}")
    
    
    
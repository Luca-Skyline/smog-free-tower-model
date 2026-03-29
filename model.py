import math
import random
import matplotlib.pyplot as plt

# constants, for all particles
y0 = 2.4 # initial height, meters (also height of chamber)
l = 0.85 # width of chamber, meters
v_air = -2.26 # velocity of the air (m/s)
voltage = 8500 # voltage between plates, volts
rho_a = 1.225 # air denisty (kg / m^3)
rho_p = 600 # particle density (kg / m^3)
vi = 1.39e-5 # air kinematic viscosity 
g = 9.81 # acceleration of gravity, m / s^2
q = 1.6e-14 # charge of particle, Coulombs
smog_concentration = 16e-9 # smog concentration in Hong Kong air, kg / m^3
dt = 0.000001 # time step
epsilon_naught = 8.85e-12 # permittivity of free space
WHO_guideline = 5 # who guideline for smog concentration, μg / m^3

# variables
x = []
y = []
t_list = [0]
concentration = [smog_concentration * 1e9]
average_mass = 0 # average mass of a particle


def simulateParticles(listOfParticles):    
    captured = 0
    escaped = 0
    listSize = len(listOfParticles)
    
    # initial values
    t = 0
    
    while(captured + escaped < listSize):
        
        print('List size: ', len(listOfParticles))
        for particle in listOfParticles[:]:
            # force of buoyancy    
            Ff = (1/6) * math.pi * (rho_a) * g * (particle.diameter ** 3)
            
            # relative velocity (particle vs air)
            urx = particle.velX
            ury = particle.velY - v_air
            
            # force of form drag   
            Fdx = -3 * vi * rho_a * math.pi * particle.diameter * urx
            Fdy = -3 * vi * rho_a * math.pi * particle.diameter * ury
            
            # force of electric field from plate
            Eplate = q * voltage / l
            
            # force of electric field from other particles
            c = (smog_concentration / average_mass) * ((listSize - captured - escaped) / listSize)
            Ecloud = (q ** 2) * c * ((2 * particle.posX) - l) / (2 * epsilon_naught)
            
            # force of gravity
            W = -1 * particle.mass * g
            
            # instantaneous acceleration from Newton's second law
            ax = (Fdx + Eplate + Ecloud) / particle.mass
            ay = (Fdy + Ff + W) / particle.mass
            
            
            # apply Euler's method to velocity and position
            particle.velX += ax * dt
            particle.velY += ay * dt
            particle.posX += particle.velX * dt
            particle.posY += particle.velY * dt
            
            if(t % 100 == 0):
                x.append(particle.posX)
                y.append(particle.posY)
            
            if(particle.posX <= 0 or particle.posX >= l):
                print('captured')
                captured += 1
                listOfParticles.remove(particle)
                t_list.append(t * dt)
                concentration.append(1e9 * smog_concentration * ((listSize - captured) / listSize))
            elif(particle.posY <= 0):
                print('escaped')
                escaped += 1
                listOfParticles.remove(particle)
                t_list.append(t * dt)
                concentration.append(1e9 * smog_concentration * ((listSize - captured) / listSize))
                
        # increment time  
        t += 1
    
    return captured / listSize

class Particle:
    def __init__(self, posX, posY, velX, velY, diameter, mass):
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.mass = mass
        self.diameter = diameter

def generateParticles(totParticles):
    totParticles += 1

    listOfParticles = []
    numPm25 = int(totParticles * (14 + 19) / (14 + 19 + 24 + 29)) #ratio of pm2.5 particles
    numPm10 = int(totParticles * (24 + 29) / (14 + 19 + 24 + 29)) # ratio of pm10 particles

    # generate pm2.5 particles
    for i in range(0, numPm25):
        p = generateSingleParticle(1 * pow(10, -6), 2.5 * pow(10, -6))
        listOfParticles.append(p)
         
    # generate pm 10 particles
    for i in range(0, numPm10):
        p = generateSingleParticle(2.5 * pow(10, -6), 10.0 * pow(10, -6))
        listOfParticles.append(p)

    return listOfParticles

def generateSingleParticle(diamMin, diamMax):
    diameter = random.uniform(diamMin, diamMax)
    posX = random.uniform(0, l)
    mass = (1 / 6) * math.pi * rho_p * pow(diameter, 3)
    p = Particle(posX, y0, 0, v_air, diameter, mass)
    return p

ps = generateParticles(20)
for particle in ps:
    average_mass += particle.mass / len(ps)
results = simulateParticles(ps)

print(results)

for p in ps:
    print(f" {p.posX:.2f} - {p.diameter} - {p.mass}")
    
plt.scatter(x,y, s=4)
plt.xlim(-0.05,l+0.05)
plt.ylim(0,y0+0.2) 
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

plt.plot(t_list,concentration)
plt.plot([0,t_list[-1]],[WHO_guideline, WHO_guideline])
plt.show()


    
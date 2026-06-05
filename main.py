import random
import math

SET = " .:-=+*#%@"
WIDTH = 80
HEIGHT = 40
OCTAVE = 4 # This is how "loud" the noise is basically think a music nnote and how they gotthat shape thing
SCALE = 0.1

PERMUTATION_TABLE = list(range(256))
random.shuffle(PERMUTATION_TABLE)
PERMUTATION_TABLE = PERMUTATION_TABLE+PERMUTATION_TABLE

def fade_curve(t): return t * t * t * (t * (t * 6 - 15) + 10) # this is from ken perlins math equation

# lerp(a,b,t) = a + 1 * (b-a) = (1-t)*a+t*b = a+t*(b-a)
def lerp(a,b,t): return a+t*(b-a)

#def get_distance_vector(x,y,dx,dy): return [x-dx,y-dy]

#given a corner of the grid cell, how much does that corner "push" the noise value at point (x, y)?
def gradiant_function(hash,x,y):
    ha = hash & 3
    if ha == 0: return x + y
    if ha == 1: return -x + y
    if ha == 2: return x - y
    if ha == 3: return -x - y

def twodnoise(x,y):
    xi = math.floor(x) & 255
    yi = math.floor(y) & 255
    xf = x - math.floor(x)
    yf = y - math.floor(y)

    fadex = fade_curve(xf)
    fadey = fade_curve(yf)
    
    bottomleft = PERMUTATION_TABLE[PERMUTATION_TABLE[xi]+yi]
    bottomright = PERMUTATION_TABLE[PERMUTATION_TABLE[xi+1]+yi]
    topleft = PERMUTATION_TABLE[PERMUTATION_TABLE[xi]+yi+1]
    topright = PERMUTATION_TABLE[PERMUTATION_TABLE[xi+1]+yi+1]

    x1 = lerp(gradiant_function(bottomleft,xf,yf), gradiant_function(bottomright,xf-1,yf),fadex)
    x2 = lerp(gradiant_function(bottomright,xf,yf-1), gradiant_function(topright,xf-1,yf-1),fadex)

def FBM():
    pass

def terrain_generation(lacunarity, persistence):

    result = 0.0
    '''
    result(x, y) = Σ noise(x * L^i, y * L^i) * P^i
                   i=0 to octaves-1
    
    this is per layer

    L = lacunarity (default 2.0)
    P = persistence (default 0.5)
    i = current octave index (0, 1, 2, 3...)
    Σ = sum all octaves together

    thx claude for formula
    '''

    for x in range(HEIGHT):
        line = ""
        for y in range(WIDTH):
            result = noise()
    

terrain_generation()
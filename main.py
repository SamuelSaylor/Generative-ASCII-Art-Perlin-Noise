import random
import math
import os
import time

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
    x2 = lerp(gradiant_function(topleft,xf,yf-1), gradiant_function(topright,xf-1,yf-1),fadex)

    return lerp(x1,x2,fadey)

def FBM(x,y,lacunarity = 2.0, persistence = 0.5):
    result = 0.0
    amplitude = 1.0
    frequency = 1.0
    for i in range(OCTAVE):
        result+=twodnoise(x*frequency,y*frequency)*amplitude
        amplitude*=persistence
        frequency*=lacunarity
    return result

def terrain_generation(offset = 0.0):

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
            result = FBM(x*SCALE,y*SCALE)
            normalization = (result+1)/2
            normalization = max(0.0,min(1.0,normalization))
            line+=SET[int(normalization*len(SET)-1)]
        print(line)
    
offset = 0.0
while True:
    os.system("cls")
    terrain_generation(offset=offset)
    offset+=0.5
    time.sleep(0.05)
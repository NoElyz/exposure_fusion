from PIL import Image
from math import sqrt
from math import exp

def imMono(image):
    im = image.convert('RGB')
    size = im.size
    im_mono = Image.new('P',size)
    for x in range(size[0]):
        for y in range(size[1]):
            im_mono.putpixel((x,y),round(sum(im.getpixel((x,y)))/3.0))
    return im_mono

#Contrast
def imC(image):
    im_mono = imMono(image)
    size = im_mono.size
    C = [[0 for y in range(size[1])] for x in range(size[0])]
    for x in range(size[0]):
        for y in range(size[1]):
            n = im_mono.getpixel((x,y))/256
            if x-1 >= 0:
                C[x-1][y] = C[x-1][y]-n
            if x+1 < size[0]:
                C[x+1][y] = C[x+1][y]-n
            if y-1 >= 0:
                C[x][y-1] = C[x][y-1]-n
            if y+1 < size[1]:
                C[x][y+1] = C[x][y+1]-n
            C[x][y] = C[x][y]+4*n
    for x in range(size[0]):
        for y in range(size[1]):
            if C[x][y] < 0:
                C[x][y] = -C[x][y]
    return C

# Saturation
def imS(image):
    im = image.convert('RGB')
    size = im.size
    S = [[0 for y in range(size[1])] for x in range(size[0])]
    for x in range(size[0]):
        for y in range(size[1]):
            r,g,b = map(lambda x:x/256,im.getpixel((x,y)))
            mu = (r+g+b)/3.0
            S[x][y] = sqrt((r-mu)**2+(g-mu)**2+(b-mu)**2)
    return S

# Well-exposedness
def imE(image):
    im = image.convert('RGB')
    size = im.size
    E = [[0 for y in range(size[1])] for x in range(size[0])]
    for x in range(size[0]):
        for y in range(size[1]):
            r,g,b = map(lambda x:x/256,im.getpixel((x,y)))
            sig = 0.2
            Er = exp(-0.5*(r-0.5)**2/sig**2)
            Eg = exp(-0.5*(g-0.5)**2/sig**2)
            Eb = exp(-0.5*(b-0.5)**2/sig**2)
            E[x][y] = Er*Eg*Eb
    return E

#!/usr/bin/python3
import sys
from converter import *

def main(argvs):
    argc = len(argvs)
    if (argc < 2):
        print ("Usage: # python %s [filename1] [filename2] [...]" % argvs[0])
        quit()

    print ("Fuse multiple photos: %s" % ' '.join(argvs[1:])) 
     
    pics = []
    for i in range(argc-1):
        pics.append(Image.open(argvs[1+i]))

    size = pics[0].size

    weights = [imW(Image.open(argvs[1+i])) for i in range(argc-1)]
    weights_sum = [[0 for y in range(size[1])] for x in range(size[0])]
    for x in range(size[0]):
        for y in range(size[1]):
            for k in range(argc-1):
                weights_sum[x][y] += weights[k][x][y]

    out = [[[0,0,0] for y in range(size[1])] for x in range(size[0])]
    for x in range(size[0]):
        for y in range(size[1]):
            for k in range(argc-1):
                RGB = pics[k].getpixel((x,y))
                for i in range(3):
                    out[x][y][i] += (weights[k][x][y]/weights_sum[x][y])*RGB[i]
                    
    image_out = Image.new('RGB',size)
    for x in range(size[0]):
        for y in range(size[1]):
            image_out.putpixel((x,y),(tuple(map(round,out[x][y]))))
    image_out.show()
    image_out.save("new.png",'PNG')

if __name__ == "__main__":
    main(sys.argv)

#Ryan Yang, 10/26/2020
#Description
#Sources:
#On my honor, I have neither given nor received personal aid

import random
import math
import cmath
from PIL import Image, ImageDraw
import numpy as np


xdim = 2**11
ydim = xdim

image = Image.new("RGB",(xdim,ydim))

max_steps = 25
thresh = 4

def get_rounds(c:complex, zinit:complex = 0) -> int:
    z=zinit
    i=0
    while (i<max_steps) and (abs(z) <thresh):
        z=z*z +c
        i+=1
    return i

xmin = -2
xmax = 2
ymin = -2
ymax = 2

set_int = []
set_size = 0
for x in range(xdim):
	for y in range(ydim):
		mx = x * (xmax-xmin)/(xdim) + xmin#converting into range from -2 to 2
		my = y * (ymax-ymin)/(ydim) + ymin#converting into range from -2 to 2
		r = get_rounds(complex(mx,my)) #i just want to be able to print out the number of iterations needed
		#r = int(mandelbrot(mx,my,0,0,0))
		#print(f"x: {mx} y: {my} rounds: {r}")
		if r >= 25:
			set_int.append(complex(x,y))
			set_size+=1
		image.putpixel((x,y),(int(256/max_steps*r),0,0))

#image.save("mandelbrot.png", "PNG")
#image.show()


#for orientation, we are projecting q to the origin. Then, val is actually the determinant of the matrix with column vectors p-q and r-q
def orientation(p:complex, q:complex, r:complex):
    ''' 
    To find orientation of ordered triplet (p, q, r).  
    The function returns following values  
    0 --> p, q and r are colinear  
    1 --> Clockwise  
    2 --> Counterclockwise  
    '''
    val = (q.imag - p.imag) * (r.real - q.real) - (q.real - p.real) * (r.imag - q.imag) 
  
    if val == 0: 
        return 0
    elif val > 0: 
        return 1
    else: 
        return 2	

def jarvis(S):
    # S is the set of points
    # P will be the set of points which form the convex hull. Final set size is i.
    pointOnHull = complex(0,ydim/2) # which is guaranteed to be part of the CH(S). This is a well known leftmost point of the Mandelbrot set
    i = 0
    P = []
    while True:
        P.append(pointOnHull)
        endpoint = S[0]      # initial endpoint for a candidate edge on the hull
        for j in range(set_size):
            # endpoint == pointOnHull is a rare case and can happen only when j == 1 and a better endpoint has not yet been set for the loop
            if (endpoint == pointOnHull) or (orientation(S[j], pointOnHull, endpoint) == 1): 
            	endpoint = S[j]   # found greater left turn, update endpoint
        i += 1
        pointOnHull = endpoint
        print(str(i))
        if endpoint == P[0]:
        	print("YES")
        	return P

#print(set_int)
print(set_size)

ch = jarvis(set_int)
cimage = Image.new("RGB",(xdim,ydim))

for k in range(len(ch)):
	cimage.putpixel((int(ch[k].real),int(ch[k].imag)),(0,128,0))
#cimage.show()

#convex_image = Image.new("RGB",(xdim,ydim))
#draw = ImageDraw.Draw(convex_image)
draw = ImageDraw.Draw(image)

ch_condensed = ()
for n in range(len(ch)):
	ch_condensed += (int(ch[n].real),int(ch[n].imag))
print(ch_condensed)
#draw.polygon(ch_condensed,fill=128)
del draw

#convex_image.show()
image.show()



# im = Image.new("RGB",(xdim,ydim))

# draw = ImageDraw.Draw(im)
# draw.line((0, 0) + im.size, fill=128)
# print((0,0)+im.size)
# draw.line((0, im.size[1], im.size[0], 0), fill=128)
# del draw

# # write to stdout
# im.show()


#111374 points needed for 1024x1024


# def complexRecursive(c,z=complex(0,0), iterations = 0):
# 	newz = z*z + c
# 	iterations +=1
# 	if abs(newz) > 2 or iterations >= max_iterations:
# 		return iterations
# 	return mandelbrot(c, newz, iterations)

# def mandelbrot(cx,cy, zx = 0, zy = 0, iterations = 0) -> int:
# 	x = zx**2 - zy**2 + cx
# 	y = 2*zx*zy + cy
# 	i = iterations+1
# 	#print(f"x: {x} y: {y}")
# 	if (i >= max_steps) or (x*x + y*y >= 4):
# 		return i
# 	return mandelbrot(cx,cy,x,y,i)
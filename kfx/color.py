import math

def rescale(color1,color2,alpha):
    if(alpha <0 ):
        return
    if(alpha >1 ):
        return
    if(len(color1) != len(color2)):
        return
    if(len(color1) != 3):
        return
    color = [0,0,0]
    alpha_star = 1 - (alpha)*(1-alpha)

    for i in range(3):
        # color[i] = math.floor(math.sqrt(color1[i]**2 * alpha + color2[i]**2 * (1-alpha)))
        color[i] = math.floor(math.exp(math.log(color1[i]+1) * alpha + math.log(color2[i]+1) * (1-alpha))-1)
        # color[i] = math.floor(math.log(math.exp(color1[i]+1) * alpha + math.exp(color2[i]+1) * (1-alpha))-1)
    return((color[0],color[1],color[2]))

#imports
import random, math
from numpy import copy
from PIL import Image, ImageDraw, ImageFont

#parameters freely changable
pcount=15
wmin=1
wmax=8

#modelling: points array
points=[]
for i in range(pcount):
    points.append(i)

#modelling: nodes 2d array -> [<start>,<end>]
nodes=[]
ncount=random.randint(1,int((pcount-1)*pcount/2)) #edges = n(n-1)/2 = binomial coefficent of (n, 2)
for i in range(ncount):
    #repeat until node is valid
    correct = False
    while not correct:
        node=[random.choice(points),random.choice(points)]
        #   lower number is first   and   node is new 
        if (node[0]<node[1])and(node not in nodes):
            nodes.append(node)
            correct=True
#weighting the nodes
for item in nodes:
    item.append(random.randint(wmin,wmax))
#end and start point, jrny stands for journey
jrny=[0,0]
while jrny[0]==jrny[1]:
    jrny=[random.choice(points),random.choice(points)]
#lower is first
if jrny[0]>jrny[1]:
    jrny[0],jrny[1]=jrny[1],jrny[0]

#functions for the path seeking loop

#check if finished by comapring the last elements of all paths to the end point
def done():
    for item in paths:
        if item[-1]!=jrny[1]:
            return False
    return True

#possible points to get to
def get_possible(p):
    result=[]
    for item in nodes:
        if item[0]==p: result.append(item[1])
        if item[1]==p: result.append(item[0])
    return result

#check if path has repetition
def repeats(pa):
    temp=[]
    for item in pa:
        if item in temp:
            return True
        else:
            temp.append(item)    
    return False

#check if its possible to continue on any path
def impossible():
    for item in paths:
        poss=get_possible(item[-1])
        for jtem in poss:
            if jtem not in item: return False
    return True

#find paths
paths=[[jrny[0]]] #inital path = start point
found=False
w=0 #idx used for debugging

print(f"-finding paths(trough {len(nodes)} nodes)-")
while not done():
    #make the paths array empty if no path is possible and exit
    if not found and impossible():
       paths=[]
       break 

    l=len(paths) #store original length
    for i in range(l):
        if paths[i][-1]!=jrny[1]: #skipping finished paths
            poss=get_possible(paths[i][-1]) #storing possible paths
            #append all possible continuations
            for j in range(len(poss)):
                path=paths[i].copy(); path.append(poss[j])
                paths.append(path)
    #clearing the array of continued or repeating paths
    to_pop=[]
    for i in range(l): #fresh paths will only appear after the original length, so we can pop any unfinished before that
        if paths[i][-1]!=jrny[1]:
            to_pop.append(paths[i])
    for item in to_pop:
        paths.remove(item)
    to_pop=[]
    #pop repeats
    for i in range(len(paths)): 
        if (paths[i][-1]!=jrny[1]) and repeats(paths[i]):
            to_pop.append(paths[i])
    for item in to_pop:
        paths.remove(item)
    
    #check if search done
    for item in paths: 
        if item[-1]==jrny[1]:
            found=True
    print(w,len(paths),sep="  > ")
    w+=1

#count weigths

#get weight of node by start and end function
def get_node(s,e):
    for item in nodes:
        if s==item[0] and e==item[1]:   
            return item
#sum each
totals=[] #store totals
for item in paths:
    d=0 #store sum
    for i in range(len(item)-1):
        start=item[i]
        end=item[i+1]
        #making sure lower is first
        if start>end:
            start,end=end,start
        d+=get_node(start,end)[2]
    totals.append(d)

#find ligthest/shortest
if found: 
    shortest=min(totals) 
    shortest_idxs=[]
    for i in range(len(totals)):
        if totals[i]==shortest: 
            shortest_idxs.append(i)

#visualizer functions
def ndconnect(nd):
    d0=math.radians(360*(nd[0]+1)/len(points))
    d1=math.radians(360*(nd[1]+1)/len(points))
    sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
    ep=(100*math.cos(d1)+128,100*math.sin(d1)+128)
    ImageDraw.Draw(img).line((sp,ep),"aqua",width=1)

def pmark(p):
    if p in jrny:
        color="green"
    else:
        color="red"
    d0=math.radians(360*(p+1)/len(points))
    sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
    ImageDraw.Draw(img).circle(sp,8,color)
    ImageDraw.Draw(img).text(sp,str(p),"blue",anchor="mm",font=font,stroke_width=0)
    

def ndmark(nd):
    d0=math.radians(360*(nd[0]+1)/len(points))
    d1=math.radians(360*(nd[1]+1)/len(points))
    sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
    ep=(100*math.cos(d1)+128,100*math.sin(d1)+128)
    d=4
    ImageDraw.Draw(img).text(((sp[0]+ep[0])/2,(sp[1]+ep[1])/2),str(nd[2]),"orange",anchor="mm",font=font,stroke_width=1)

def draw_path(pa):
    for i in range(len(pa)-1):
        d0=math.radians(360*(pa[i]+1)/len(points))
        d1=math.radians(360*(pa[i+1]+1)/len(points))
        sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
        ep=(100*math.cos(d1)+128,100*math.sin(d1)+128)
        ImageDraw.Draw(img).line((sp,ep),"purple",width=3)

#visualizing
img=Image.new("RGB",(256,256),"white")
font=ImageFont.truetype("arial.ttf",16)
for item in nodes:
    ndconnect(item)
if found: 
    for item in shortest_idxs:
        draw_path(paths[item])
for item in nodes:
    ndmark(item)
for item in points:
    pmark(item) 

img.save("dijkstra\djikstra.png")

#result report
print("-"*8)
print(f"nodes: {nodes}")
print(f"journey: {jrny}")
print("end results:")
if found:
    print(f"shorthest paths, with sum={shortest}:")
    for i in range(len(totals)):
        if totals[i]==shortest: print(paths[i])
else: print("no possible path")
print("-"*8)


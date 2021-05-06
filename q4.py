import json
from copy import deepcopy
import sys

with open(sys.argv[1]) as f:
    dfa=json.load(f)

flag=False
while flag == False:
    # print("htrt")
    for x in dfa["states"]:
        ie=oe=0
        for j in dfa["transition_function"]:
            if x==j[0] and x == j[2]:
                pass
            elif x == j[2]:
                ie+=1
            elif x==j[0]:
                oe+=1
        if (ie ==0 and oe ==0):
            if x in dfa['states']:
                dfa["states"].remove(x)
            if x in dfa["final_states"]:
                dfa["final_states"].remove(x)
            if x in dfa["start_states"]:
                dfa["start_states"].remove(x)
                # flag=True
                # break
        else:
            if (oe==0 and x not in dfa["final_states"]) or (ie ==0 and x not in dfa["final_states"] and x not in dfa["start_states"]):
                flag=True
                # print(x)
                toremove=[]
                for y in dfa["transition_function"]:
                    if x in y:
                        toremove.append(y)
                for i in toremove:
                    dfa["transition_function"].remove(i)
                dfa["states"].remove(x)
                if x in dfa["final_states"]:
                    dfa["final_states"].remove(x)
    if flag==True:
        flag=False
    else:
        flag=True

# print(dfa)
newletters=set()
for x in dfa["transition_function"]:
    newletters.add(x[1])
dfa["letters"]=list(newletters)
def returnIndex(y):
    global previousp1
    for i in range(len(previousp1)):
        if y in previousp1[i]:
            return i

def checkDistinguishable(x):
    if x == []:
        return True
    global dfa
    global mp1
    global mp2
    global transition_table
    mp={}
    for y in x:
        mp[y]=[]
        for xt in dfa["letters"]:
            x1=transition_table[mp2[y]][mp1[xt]]
            x1=returnIndex(x1)
            mp[y].append(x1)
    
    c=mp[x[0]]
    for key in mp:
        if mp[key]!=c:
            return False
    return True

def getpartition(x):
    l=1<<len(x)
    for i in range(l//2):
        s1=[]
        s2=[]
        for j in range(len(x)):
            if i & (1<<j):
                s1.append(x[j])
            else:
                s2.append(x[j])
        f1=checkDistinguishable(s1)
        f2=checkDistinguishable(s2)
        if f1==True and f2==True:
            return s1,s2
    

def getTransitState(x,y):
    global transition_table
    global previousp
    global previousp1
    global mp1
    global mp2
    c=transition_table[mp2[x]][mp1[y]]
    for i in range(len(previousp1)):
        if c in previousp1[i]:
            return previousp[i]

def checkForEqualTransitions(x):
    global transition_table
    global mp2
    mp={}
    for xt in x:
        tt=[]
        for r in transition_table[mp2[xt]]:
            if r!='$':
                tt.append('-')
            else:
                tt.append('$')
        exp=''.join(tt)
        # print(exp)
        if exp in mp:
            mp[exp].append(xt)
        else:
            mp[exp]=[xt]
    fs=[]
    for key in mp:
        fs.append(mp[key])
    return fs 

transition_table = [['$' for x in dfa["letters"]] for y in dfa["states"]]
mp1={}
start=0
for i in dfa["letters"]:
    mp1[i]=start
    start+=1
start=0
mp2={}
for i in dfa["states"]:
    mp2[i]=start
    start+=1
for x in dfa["transition_function"]:
    transition_table[mp2[x[0]]][mp1[x[1]]]=mp2[x[2]]

previousp=[]
p0=[]
startstates=dfa["states"]
for x in dfa["final_states"]:
    startstates.remove(x)
startstates=checkForEqualTransitions(startstates)
l=checkForEqualTransitions(dfa["final_states"])
p0=startstates
for i in l:
    p0.append(i)
p=0
previousp=p0
# print(mp2)
# print(transition_table)
# print(previousp)       
while True:
    # print(previousp)
    p+=1
    nextstate=[]
    previousp1=deepcopy(previousp)
    for x in range(len(previousp1)):
        for y in range(len(previousp1[x])):
            previousp1[x][y]=mp2[previousp1[x][y]]
    # print(previousp1)
    for x in previousp:
        s1,s2=getpartition(x)
        # print(s1,s2,"awdwad")
        if s2 == []:
            nextstate.append(s1)
        elif s1 == []:
            nextstate.append(s2)
        else:
            nextstate.append(s1)
            nextstate.append(s2)
    
    if nextstate == previousp:
        break
    else:
        previousp=deepcopy(nextstate)
        nextstate=[]

newdfa={}
newdfa['states']=previousp
newdfa['letters']=dfa['letters']
newdfa['transition_function'] = []
newdfa['start_states']=[]
newdfa['final_states']=[]
ss=[]
fs=[]
for i in dfa['start_states']:
    for j in previousp:
        if (i in j) and (j not in ss):
            ss.append(j)
for i in dfa['final_states']:
    for j in previousp:
        if (i in j) and (j not in fs):
            fs.append(j)
for i in previousp:
    for j in dfa['letters']:
        u=getTransitState(i[0],j)
        if u:
            newdfa["transition_function"].append([i,j,u])

newdfa['start_states']=ss
newdfa['final_states']=fs
with open(sys.argv[2],"w") as f:
    json.dump(newdfa,f)
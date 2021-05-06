import json
from copy import deepcopy
import sys
def calculateIncomingAndOutgoingEdges(intermediateStates):
    global dfa
    mp=[]
    for x in intermediateStates:
        ie=oe=0
        for j in dfa["transition_function"]:
            if j[2] == x:
                ie+=1
            elif j[0] == x:
                oe+=1
        mp.append([x,(ie,oe)])
    return mp

def getAllTransitions(xt):
    global dfa
    lis=[]
    for x in dfa["transition_function"]:
        if xt in x:
            lis.append(x)
    incoming=[]
    outgoing=[]
    selfloop=[]
    for x in lis:
        if xt == x[0] and xt!=x[2]:
            outgoing.append(x)
        elif xt == x[2] and xt!=x[0]:
            incoming.append(x)
        else:
            selfloop.append(x)
    return incoming,outgoing,selfloop

def clearOldTransitions(r):
    global dfa
    for x in r:
        if x in dfa["transition_function"]:
            dfa["transition_function"].remove(x)

with open(sys.argv[1]) as f:
    dfa=json.load(f)
if len(dfa["final_states"])>1:
    for x in dfa["final_states"]:
        dfa["transition_function"].append([x,'$','Qf'])
    
    dfa["final_states"]=["Qf"]

startstate=dfa["start_states"][0]
for x in dfa["transition_function"]:
    if startstate == x[2]:
        dfa["transition_function"].append(["Qi","$",startstate])
        startstate="Qi"
        dfa["start_states"][0]="Qi"
        break

finalstate=dfa["final_states"][0]
for x in dfa["transition_function"]:
    if finalstate == x[0]:
        dfa["transition_function"].append([finalstate,"$","Qf"])
        dfa["final_states"]=["Qf"]
        break

intermediateStates=deepcopy(dfa["states"])
if dfa["start_states"][0] in intermediateStates:
    intermediateStates.remove(dfa["start_states"][0])
if dfa["final_states"][0] in intermediateStates:
    intermediateStates.remove(dfa["final_states"][0])
ieedges = calculateIncomingAndOutgoingEdges(intermediateStates)
ieedges.sort(key=lambda a:a[1][0]+a[1][1])
while len(dfa["transition_function"])!=1 and len(intermediateStates)>0:
    # print(dfa["transition_function"])
    stateToRemove=ieedges[0][0]
    inc,out,selfloops=getAllTransitions(stateToRemove)
    # print(selfloops)
    exp=[]
    if len(selfloops) > 1:
        exp=[]
        for lo in selfloops:
            exp.append(lo[1])
            exp.append('+')
        exp.pop()
        exp=''.join(exp)
        # dfa["transition_function"].append([stateToRemove,exp,stateToRemove])
    elif len(selfloops) == 1:
        exp=selfloops[0][1]
    else:
        exp=''
    for x in inc:
        for y in out:
            if exp == "":
                dfa["transition_function"].append([x[0],"{}{}".format(x[1],y[1]),y[2]])
            elif len(exp) == 1:
                dfa["transition_function"].append([x[0],"{}{}*{}".format(x[1],exp,y[1]),y[2]])
            else:
                dfa["transition_function"].append([x[0],"{}({})*{}".format(x[1],exp,y[1]),y[2]])
    clearOldTransitions(inc)
    clearOldTransitions(out)
    clearOldTransitions(selfloops)
    # print(stateToRemove)
    intermediateStates.remove(stateToRemove)
    ieedges = calculateIncomingAndOutgoingEdges(intermediateStates)
    ieedges.sort(key=lambda a:a[1][0]+a[1][1])

fg=[]
for x in dfa["transition_function"]:
    fg.append(x[1])
    fg.append('+')

fg.pop()
fg=''.join(fg)
# print(fg)
# print(dfa["transition_function"])
dfa["transition_function"] = [[dfa["transition_function"][0][0],fg,dfa["transition_function"][0][2]]]
# print(dfa["transition_function"])
finalregex = [x for x in dfa["transition_function"][0][1] if x!='$']
regex={}
regex['regex']=''.join(finalregex)
# print(regex['regex'])
with open(sys.argv[2],'w') as f:
    json.dump(regex,f)
import json
import sys
from copy import deepcopy
with open(sys.argv[1]) as f:
	nfa=json.load(f)
# print(nfa)
def getlistOfTransitions(xt):
    global nfa
    lis=[]
    # print(nfa["transition_function"])
    for k in nfa["transition_function"]:
        if k[0] == xt:
            lis.append([k[1],k[2]])
    return lis

def getTransitionState(x):
    mp={}
    for y in x:
        lis=getlistOfTransitions(y)
        for j in lis:
            if j[0] in mp:
                if j[1] not in mp[j[0]]:
                    mp[j[0]].append(j[1])
            else:
                mp[j[0]]=[]
                mp[j[0]].append(j[1])
    # print(mp)
    return mp

dfa={}
dfa["states"]=[]
dfa["letters"]=nfa["letters"]
dfa["transition_function"]=[]
dfa["start_states"]=[]
for i in nfa["start_states"]:
    dfa["start_states"].append([i])
# dfa["start_states"]=nfa["start_states"]
dfa["final_states"]=[]
states=[]
x=len(nfa["states"])
x=1<<x
for i in range(x):
    pstate=[]
    for j in range(len(nfa["states"])):
        if i & (1<<j):
            pstate.append(nfa["states"][j])
    states.append(pstate)
# print(states)
for x in states:
    if x == []:
        for t in nfa["letters"]:
            dfa["transition_function"].append([[],t,[]])
        continue
    l=getTransitionState(x)
    for key in l:
        l[key].sort(key=lambda x:int(x[1:len(x)]))
        dfa["transition_function"].append([x,key,l[key]])
    for key in nfa["letters"]:
        if key not in l:
            dfa["transition_function"].append([x,key,[]])

dfa["states"]=states
finalstates=set({})

for x in nfa["final_states"]:
    for j in dfa["transition_function"]:
        if x in j[2]:
            finalstates.add(tuple(j[2]))
        if x in j[0]:
            finalstates.add(tuple(j[0]))

finalstates=[list(x) for x in finalstates]
# print(finalstates)
dfa["final_states"]=finalstates
with open(sys.argv[2],'w') as f:
	json.dump(dfa,f)
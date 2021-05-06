import json
import sys
states=0
letters=set({})
def isLetterOrDigit(y):
	if (y>=48 and y<=57) or (y>=97 and y<=122):
		return True
	return False

def getPrecedence(ch):
	if ch == '*':
		return 2
	elif ch == '+':
		return 1
	elif ch == '.':
		return 3
	elif ch == '(':
		return 4

def shuntingyard(x):
	stack=[]
	outstring=""
	for i in range(len(x)):
		# print(outstring)
		ch=x[i]
		if isLetterOrDigit(ord(ch)):
			outstring+=ch
		elif ch == '(':
			stack.append(ch)
		elif ch == ')':
			while len(stack)>0 and stack[len(stack)-1]!='(':
				outstring+=stack[len(stack)-1]
				stack.pop()
			stack.pop()
		else:
			while len(stack)>0 and getPrecedence(ch)>=getPrecedence(stack[len(stack)-1]):
				outstring+=stack[len(stack)-1]
				stack.pop()
			stack.append(ch)
	while len(stack)>0:
		outstring+=stack[len(stack)-1]
		stack.pop()
	return outstring

def parseString(x):
	res=[]
	for i in range(len(x)-1):
		res.append(x[i])
		if isLetterOrDigit(ord(x[i])) and isLetterOrDigit(ord(x[i+1])):
			res.append('.')
		elif x[i]==')' and x[i+1] == '(':
			res.append('.')
		elif isLetterOrDigit(ord(x[i+1])) and x[i]==')':
			res.append('.')
		elif x[i+1]=='(' and isLetterOrDigit(ord(x[i])):
			res.append('.')
		elif x[i] in ['*'] and (isLetterOrDigit(ord(x[i+1]) or x[i+1] == '(')):
			res.append('.')
	if( x[len(x)-1] != res[len(res)-1]):
		res += x[len(x)-1]
	return ''.join(res)

def symbolNFA(ch):
	global states
	global letters
	letters.add(ch)
	nfa["transition_function"].append(["Q{}".format(states),ch,"Q{}".format(states+1)])
	states+=2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def unionNFA(nfa1,nfa2):
	global states
	nfa["transition_function"].append(["Q{}".format(states),'$',nfa1[0]])
	nfa["transition_function"].append(["Q{}".format(states),'$',nfa2[0]])
	nfa["transition_function"].append([nfa1[1],'$',"Q{}".format(states+1)])
	nfa["transition_function"].append([nfa2[1],'$',"Q{}".format(states+1)])
	states+=2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def loopNFA(nfa1):
	# print(nfa1)
	global states
	nfa["transition_function"].append([nfa1[1],'$',nfa1[0]])
	nfa["transition_function"].append(["Q{}".format(states),'$',nfa1[0]])
	nfa["transition_function"].append([nfa1[1],'$',"Q{}".format(states+1)])
	nfa["transition_function"].append(["Q{}".format(states),'$',"Q{}".format(states+1)])
	states+=2
	return ["Q{}".format(states-2),"Q{}".format(states-1)]

def concatNFA(nfa1,nfa2):
	global states
	nfa["transition_function"].append([nfa1[1],'$',nfa2[0]])
	return [nfa1[0],nfa2[1]]	

def regexToNFA(x):
	stack=[]
	xt=""
	for i in range(len(x)):
		if isLetterOrDigit(ord(x[i])):
			stack.append(symbolNFA(x[i]))
		elif x[i] == '+':
			xt=unionNFA(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop()
			stack.pop()
			stack.append(xt)
		elif x[i] == "*":
			xt=loopNFA(stack[len(stack)-1])
			stack.pop()
			stack.append(xt)
		else:
			xt=concatNFA(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop()
			stack.pop()
			stack.append(xt)
	nfa["start_states"]=[xt[0]]
	nfa["final_states"]=[xt[1]]

with open(sys.argv[1]) as f:
	x=json.load(f)
x=x["regex"]
nfa={}
nfa["states"]=[]
nfa["letters"]=[]
nfa["transition_function"]=[]
x=parseString(x)
x=shuntingyard(x)
print(x)
regexToNFA(x)
# print(nfa["transition_function"])
s=set({})
for x in nfa["transition_function"]:
	s.add(x[0])
	s.add(x[2])
s=list(s)
s.sort(key=lambda a:int(a[1:]))
nfa["states"]=s
nfa["letters"]=list(letters)
# print(nfa)
with open(sys.argv[2],'w') as f:
	json.dump(nfa,f)

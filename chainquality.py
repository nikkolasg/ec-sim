import networkx as nx
import numpy as np 
import itertools

nh=67 #number of honest players
na=33#number of adversarial players
ntot=na+nh #total num,ber of players
p=1./float(ntot) #proba for one leader to be elected
Kmax=40 #length of the attack
grind_max=30 #how many "grinds" we allow
sim=100 #number of simulations
forks=[]

### How many times does the adversary have a longest chain than honest chain with 33% of power?


### Grinding:
def grind(n):
	index_parent = n
	lgth = G.node[n]['length']
	c = G.node[n]['num_winner']
	slot = G.node[n]['slot']
	global ct
	global current_list
	if slot<Kmax:
		for i in range(grind_max):
			ca = np.random.binomial(na*c, p, 1)[0]
			j=slot+i+1
			if ca>0 and j<Kmax:
				ct+=1
				G.add_node(ct,slot=j,length=lgth+1,num_winner=ca,parent=n)
				G.add_edge(index_parent,ct)
				current_list.append(ct)#add all new nodes to the list
			#if no leader we need to go direct to the delay case 
		#remove n from list
	current_list.remove(n)

##adversarial fork without grinding:
forks=[]
for i in range(sim):
	nogrinding_fork_length=0
	slot_number=0
	ca = np.random.binomial(na, p, 1)[0]#honest players each toss a coin to see if elected leaders
	while slot_number<Kmax:
		if ca>0:#there were leaders elected, one block is created
			nogrinding_fork_length+=1
			#no leaders elected everyone moves to next slot
		slot_number+=1
		ca = np.random.binomial(na, p, 1)[0]#each honest leaders toss
			#a new coin for that round
	forks.append(nogrinding_fork_length)
forks_adv=[]

for i in range(sim):
	G=nx.DiGraph()
	G.add_node(0,slot=0,length=0,num_winner=1)
	ct=0
	current_list=[0]
	max_l=0
	while current_list :
		for n in current_list:
			#print(current_list)
			if G.node[n]['length']>max_l: max_l = G.node[n]['length']
			grind(n)

	forks_adv.append(max_l)

#what happens to the rest of the player?
forks_honest=[]
for i in range(sim):
	honest_fork_length=0
	slot_number=0
	ch = np.random.binomial(nh, p, 1)[0]

	while slot_number<Kmax:
		if ch>0:#there were leaders elected, one block is created
			honest_fork_length+=1
			#no leaders elected everyone moves to next slot
		slot_number+=1
		ch = np.random.binomial(nh, p, 1)[0]#each honest leaders toss
			#a new coin for that round
	forks_honest.append(honest_fork_length)


quality=[1 if forks_adv[i]>=forks_honest[i] else 0 for i in range(sim)  ]
#praosh=[1 for i in range(len(ch)) if ch[i]>0 ]

#longest chain case:
print "Adversary wins with probability: {f}. \n Without grinding\
the adversary wins with probability: {f2}".format(f=np.average(quality),\
	f2=np.average([1 if forks[i]>=forks_honest[i] else 0 for i in range(sim)  ]))
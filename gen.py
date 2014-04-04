import random

def fabs(x):
	if(x>0):	return x
	return -x

def generate(howmuch,curr,mymin,mymax):

	data=[]
	base=0.9*mymin
	curr-=base
	mymin-=base
	mymax-=base

	d1=(mymax-curr)**2
	d2=(mymin-curr)**2
	sigma=((d1+d2)/2.0)**0.4
	mean=(mymin+mymax)/2.0
	
	for i in range(0,howmuch):
		data.append(int(base+fabs(random.gauss(mean,sigma))))

	return data

print generate(10000,14,7,34)
	

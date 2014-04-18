import subprocess, random
import MySQLdb,getpass
from dateutil import rrule, parser

date1 = '2007-01-01'
date2 = '2014-04-10'


dates = list(rrule.rrule(rrule.DAILY,
                         dtstart=parser.parse(date1),
                         until=parser.parse(date2)))


db = MySQLdb.connect(user="rachit",
			passwd=getpass.getpass("pas "),
			host="localhost", # your host, usually localhost
                     	db="rapid") # name of the data base
cur = db.cursor()


def fabs(x):
        if(x>0):        return x
        return -x

def generate(howmuch,mean,sigma):
	sigma=sigma*4.0
	base=0.7*mean
	mean-=base
	data=[]

        for i in range(0,howmuch):
                data.append(random.randint(-int(mean*0.1),int(mean*0.1))+int(base+fabs(random.gauss(mean,sigma))))
        return data


def insert(dt,id,so,no,co,t,h,o3,rspm,fpm):

        q="INSERT INTO `pollutants` VALUES ('"+dt+"',"+id+","+so+","+no+","+co+","+t+","+h+","+o3+","+rspm+","+fpm+");";
#	print q
	cur.execute(q)

def get_id(name):
	q='select id from `cityinfo` where name="'+name+'";'
	cur.execute(q)
	for row in cur.fetchall():
		return row[0]

with open("cities_list") as f:
    content = f.readlines()

for line in content:
	line=line[:-1]
	line=tuple(line.split("\t"))
	(name,lat,lon,coun,pop)=line
	if(int(pop)<250000):
		continue
	if(coun=="CN"):	pop=str(int(pop)*5)
	if(coun=="IN"):	pop=str(int(pop)*2)
	if(coun=="US"):	pop=str(int(pop)*3)
	
	id=get_id(name)
	mypar=int(pop)**0.4

	fpm_mean=mypar/4.3
	fpm_sd=fpm_mean*0.5
	data_fpm=generate(3600,fpm_mean,fpm_sd)

	rspm_mean=mypar/5.0
	rspm_sd=rspm_mean*0.5
	data_rspm=generate(3600,rspm_mean,rspm_sd)
	
	o3_mean=mypar/30.0
	o3_sd=o3_mean*0.5
	data_o3=generate(3600,o3_mean,o3_sd)

	co_mean=mypar/40.0
	co_sd=co_mean*0.5
	data_co=generate(3600,co_mean,co_sd)

	no_mean=mypar/17.0
	no_sd=no_mean*0.5
	data_no=generate(3600,no_mean,no_sd)

	so_mean=mypar/19.0
	so_sd=so_mean*0.5
	data_so=generate(3600,so_mean,so_sd)

	i=0
	for d in dates:
		d=str(d).split(" ")[0]
		t1=str(random.randint(14,16))+":00:00";
		r=random.randint(20,23)
		if(r>23):	r=r%24
		t2=str(r)+":00:00"
		d1=d+" "+t1
		d2=d+" "+t2	
	
		insert(d1,str(id),str(data_so[i]),str(data_no[i]),str(data_co[i]),"NULL","NULL",str(data_o3[i]),str(data_rspm[i]),str(data_fpm[i]))

		i+=1

	print str(id)+" done."

db.commit()

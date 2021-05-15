from django.shortcuts import render
import numpy as np
import operator
from matplotlib import pyplot as plt
import pandas as pd
from django.http import HttpResponse

xcel='results.xlsx'
df=pd.read_excel(xcel)
# Create your views here.
def common(branches,Htno,Subcode,Subname,Grade,branchname):
	k={}
	c=0
	for b,v in branches.items():	
		if b==branchname:
			c+=1
			for i in range(len(Htno)):
				if str(Htno[i])[6:-2]==v and Subcode[i] not in k and c!=9:
					k[Subcode[i]]=Subname[i]
				else:
					pass
	return(k)

def hello(df):
	Htno=list(df['Htno'])
	Subcode=list(df['Subcode'])
	Subname=list(df['Subname'])
	Grade=list(df['Grade'])
	Credits=list(df['Credits'])
	lst1,lst2=[],[]
	branches={'ECE':'04','CSE':'05','IT':'12','MECH':'03','EEE':'02','CIV':'01'}
	dicc={'O':10,'S':9,'A':8,'B':7,'C':6,'D':5,'F':0,'ABSENT':0,'COMPLETED':0}
	return(Subcode,Subname,Grade,Credits,branches,dicc,Htno)
def call(Grade,Credits,dicc):
	for i,j in dicc.items():
		if Grade==i:
			ff=(j*Credits)
		else:
			continue
	return(ff)	
def apf(Subcode,reg,Htno,ht,Grade):	
	failst,abslst,passlst=0,0,0
	gg=['O','S','A','B','C','D']			
	for i in range(len(Subcode)):
		if reg==Subcode[i] and str(Htno[i])[6:-2]==ht:
			if Grade[i]=='F':
				failst+=1
			elif Grade[i]=='ABSENT' and str(Htno[i])[6:-2]==ht:
				abslst+=1
			elif Grade[i] in gg and str(Htno[i])[6:-2]==ht:
				passlst+=1	
	color1,color2,color3="#FF4500","#00FF7F","#0000FF"					
	return(reg,failst,passlst,abslst,color1,color2,color3)			
def your_rank(Htno,bb,Grade,Credits,dicc):
	f={}
	toppers=[]
	for i in range(len(Htno)):
		if str(Htno[i])[6:-2]==bb[6:-2] and Htno[i]  in f :
			f[Htno[i]]=f[Htno[i]]+call(Grade[i],Credits[i],dicc)
		elif str(Htno[i])[6:-2]==bb[6:-2] and Htno[i] not in f:
			f[Htno[i]]=call(Grade[i],Credits[i],dicc)
	f = dict( sorted(f.items(), key=operator.itemgetter(1),reverse=True))
	c,H=0,0
	for i,j in f.items():
		if H!=j:
			c+=1
			H=j
		else:
			c=c	
		if bb==i:
			return(c)

def hii(req):
	return render(req,'common.html')


def Individual_Info(req):
	Subcode,Subname,Grade,Credits,branches,dicc,Htno=hello(df)
	if req. method=='POST':
		hallticket=req.POST.get('pinn')
		hallticket=hallticket.upper()		
		subn,subc,gree,cree=[],[],[],[]
		grades,cre=0,0
		for i in range(len(Htno)):
			if Htno[i]==hallticket:
				subn.append(Subname[i])
				subc.append(Subcode[i])
				gree.append(Grade[i])
				cree.append(Credits[i])
				for k,v in dicc.items():
					if k==Grade[i]:
						cre+=Credits[i]
						grades=grades+(v*Credits[i])
		if len(subn)==0:
			return HttpResponse('go back .....Enter PIN number properly')	
		else:				
			rank=your_rank(Htno,hallticket,Grade,Credits,dicc)	
			return render(req,'pin1.html',{'subcode':subc,'subname':subn,'grades':gree,'credits':cree,'cgpa':grades/cre,'rank':rank})
	return render(req,'pin1.html')

def Branch_Det(req):
	return render(req,'branch_com.html')	
def Complete_Data(req):
	Subcode,Subname,Grade,Credits,branches,dicc,Htno=hello(df)
	f,ff,adder=[],[],0
	for b,c in branches.items():
		failst,passlst,abslst=0,0,0
		for i in range(len(Htno)):
			if c==str(Htno[i])[6:-2]:
				if Grade[i]=='F':
					failst+=1
				elif Grade[i]=='ABSENT':
					abslst+=1
				else:
					passlst+=1
		adder=failst+passlst+abslst
		color1,color2,color3="#FF4500","#00FF7F","#0000FF"
		f=[b,((failst/adder)*100),((passlst/adder)*100),((abslst/adder)*100)]
		ff.append(list(f))
	print(ff)			
	return render(req,'complete.html',{'ff':ff})
def Branch_Details(req):
	if req.method=='POST':
		bb=req.POST.get('lang')
		Subcode,Subname,Grade,Credits,branches,dicc,Htno=hello(df)
		f={}
		for b,g in branches.items():
			if bb==b:
				for i in range(len(Htno)):
					if str(Htno[i])[6:-2]==g and Htno[i]  in f :
						f[Htno[i]]=f[Htno[i]]+call(Grade[i],Credits[i],dicc)
					elif str(Htno[i])[6:-2]==g and Htno[i] not in f:
						f[Htno[i]]=call(Grade[i],Credits[i],dicc)
		f = dict( sorted(f.items(), key=operator.itemgetter(1),reverse=True))
		c,H=0,0

		cc,k,v=[],[],[]
		#print(f)
		for i,j in f.items():
			k.append(i)
			v.append(j)
			if H!=j:
				c=c+1
				cc.append(c)

				H=j
			elif H==j:
				cc.append(c)
		print(k[:10])			
		return render(req,'list.html',{'k':k,'v':v,'rank':cc})
	return render(req,'topper.html')
def passper(req):
	if req.method=="POST":
		Subcode,Subname,Grade,Credits,branches,dicc,Htno=hello(df)
		branchname=req.POST.get('lang')
		k=common(branches,Htno,Subcode,Subname,Grade,branchname)
		req.session["llst"]=k
		req.session["llst1"]=branchname
		subnames=[]
		for i,j in k.items():
			subnames.append(j)
		k='Yellow'		
		return render(req,'sub_names.html',{'h':subnames,'k':k})
	return render(req,'sub_names.html')	
def passper1(req):
	if req.method=="POST":
		Subcode,Subname,Grade,Credits,branches,dicc,Htno=hello(df)
		subname=req.POST.get('hello')
		k=req.session["llst"]
		branchname=req.session["llst1"]
		for i,j in branches.items():
			if i== branchname:
				ht=j
				break
		for c,n in k.items():
			if subname==n:
				reg=c
				break
		f=apf(Subcode,reg,Htno,ht,Grade)	
		print(f)	
		t=[]			
		t1=['failure','pass','absent']
		t.append(f[1])
		t.append(f[2])
		t.append(f[3])
		print(t,t1)
		return render(req,'subpass.html',{'t':t,'t1':t1,'reg':reg,'subname':subname})
def bnchpass(req):
	if req.method=="POST":
		Subcode,Subname,Grade,Credits,branches,dicc,Htno=hello(df)
		branchname=req.POST.get('lang')
		k=common(branches,Htno,Subcode,Subname,Grade,branchname)
		mai=[]
		for i,j in branches.items():
			if i== branchname:
				ht=j
				break
		t1=[]

		for reg,j in k.items():
			p=apf(Subcode,reg,Htno,ht,Grade)
			mai.append(list(p))	
			t1.append(reg)
		print(mai)	
		t2="ece"
		return render(req,'branchpass.html',{'mai':mai,'t1':t1,'t2':t2})
	return render(req,'topper2.html')				
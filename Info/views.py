from django.shortcuts import render
from django.http import HttpResponse
import requests
import json


def home(request):
	return render(request, 'Info/home.html')

def developer(request):
	return render(request, 'Info/Developers.html')


def index(request):
	date = request.POST.get('date',None)
	json.dump(date,open("date.txt","w"))
	
	source_code = request.POST.get('source_code',None)
	dest_code = request.POST.get('dest_code',None)
	api_key = "bawet7852"

	url = "http://api.railwayapi.com/between/source/"+str(source_code) +"/dest/"+str(dest_code)+"/date/"+str(date)+"/apikey/"+api_key+"/"
	
	r = requests.get(url=url)


	res = r.json()
	json.dump(res,open("rail.txt","w"))
	data = []
	data.append(res['train'])

	return render(request, 'Info/InfoRail.html', {'data':data})

def getavailability(request):
	level = request.POST.get('level',None)
	quota = request.POST.get('quota',None)
	number = request.POST.get('number',None)
	api_key = "bawet7852"

	url = "http://api.railwayapi.com/route/train/"+str(number)+"/apikey/"+api_key+"/"

	r = requests.get(url=url)
	res = r.json()

	route = []
	l = len(res['route'])
	
	for i in range (0,l):
		route1 = []
		route1.append(res['route'][i]['fullname'])
		route1.append(res['route'][i]['code'])
		route.append(route1)
	

	res2 = json.load(open("rail.txt"))

	frm = []
	to = []
	j = len(res2['train'])

	for i in range(0,j):
		
		frm.append(res2['train'][i]['from']['code'])
    	to.append(res2['train'][i]['to']['code'])


	t=0
	f=0
	k=0
	for i in range (0,j):
		if frm[i] == number:
			k=i

	for i in range (0,l):	
		if route[i][1] == frm[k]:	
			f=i
		if route[i][1] == to[k]:
			t=i
    
    

	l=0
	availability = []
	date = json.load(open("date.txt"))

	url = "http://api.railwayapi.com/check_seat/train/"+str(number)+"/source/" +route[f][1]+ "/dest/" +route[t][1]+"/date/"+date+"-2016/class/"+str(str(level))+"/quota/"+str(quota)+"/apikey/"+api_key+"/"
	r=requests.get(url=url)
	result=r.json()

	try:
		seat = result['availability'][0]['status']
		if seat[0:9] == "Available" or seat[0:3] == "RAC": 
			availability.append("Seat_availability from "+route[f][1]+" to "+route[t][1]+ " is : " +seat)
		else:
			l=1
	except:
		l=1 


	if l== 1:
		url = "http://api.railwayapi.com/check_seat/train/"+str(number)+"/source/" +route[f][1]+ "/dest/" +route[t-1][1]+"/date/"+date+"-2016/class/"+str(level)+"/quota/"+str(quota)+"/apikey/"+api_key+"/"
		r=requests.get(url=url)
		result=r.json()  
		try:
			seat = result['availability'][0]['status']
			if seat[0:9] == "Available" or seat[0:3] == "RAC": 
				availability.append("Seat_availability from "+route[f][1]+" to "+route[t-1][1]+ " is : " +seat)
			else:
				l=2
		except:
			l=2
	


	if l==2:
		url = "http://api.railwayapi.com/check_seat/train/"+str(number)+"/source/" +route[f+1][1]+ "/dest/" +route[t][1]+"/date/"+date+"-2016/class/"+str(level)+"/quota/"+str(quota)+"/apikey/"+api_key+"/"
		r=requests.get(url=url)
		result=r.json()  
		try:
			seat = result['availability'][0]['status']
			if seat[0:9] == "Available" or seat[0:3] =="RAC":     
				availability.append("Seat_availability from "+route[f+1][1]+" to "+route[t][1]+ " is : " + seat)
			else:
				l=3
		except:
			l=3
	

	if l==3:
		url = "http://api.railwayapi.com/check_seat/train/"+str(number)+"/source/" +route[f+1][1]+ "/dest/" +route[t-1][1]+"/date/"+date+"-2016/class/"+str(level)+"/quota/"+str(quota)+"/apikey/"+api_key+"/"
		r=requests.get(url=url)
		result=r.json()  
		try:
			seat = result['availability'][0]['status']
			if seat[0:9] == "Available" or seat[0:3] =="RAC":     
				availability.append("Seat_availability from "+route[f+1][1]+" to "+route[t-1][1]+ " is : " + seat)
			else:
				l=4
		except:
			l=4
	

	if l==4:
		url = "http://api.railwayapi.com/check_seat/train/"+str(number)+"/source/" +route[f-1][1]+ "/dest/" +route[t][1]+"/date/"+date+"-2016/class/"+str(level)+"/quota/"+str(quota)+"/apikey/"+api_key+"/"
		r=requests.get(url=url)
		result=r.json()                                                                                                                                   
		try:
			seat = result['availability'][0]['status']
			if seat[0:9] == "Available" or seat[0:3] =="RAC":
				availability.append("Seat_availability from "+route[f-1][1]+" to "+route[t][1]+ " is : " + seat)
			else:
				l=5
		except:
			l=5
	

	if l==5:
		url = "http://api.railwayapi.com/check_seat/train/"+str(number)+"/source/" +route[f-1][1]+ "/dest/" +route[t+1][1]+"/date/"+date+"-2016/class/"+str(level)+"/quota/"+str(quota)+"/apikey/"+api_key+"/"
		
		r=requests.get(url=url)
		result=r.json()
		try:
			seat = result['availability'][0]['status']
			if seat[0:9] == "Available" or seat[0:3] =="RAC":      
				availability.append("Seat_availability from "+route[f-1][1]+" to "+route[t+1][1]+ " is : " + seat)
			else:
				l=6
		except:
			availability.append("Sorry there is no ticket available in this class")
	

	if l==6:
		availability.append("Sorry No ticket Available")

	
	return render(request, 'Info/ticket.html', {'route':route, 'availability':availability })


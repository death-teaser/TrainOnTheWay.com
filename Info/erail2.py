import requests
import json

print("Station code : ")
source_code = input()

print("destination code : ")
dest_code = input()

print("dd-mm : ")
date = input()

print("Enter Class ( plz enter in capital letters ) : ")
level = input()

print("Enter your quota : ")
quota = input()

api_key = "bawet7852"

url="http://api.railwayapi.com/between/source/"+source_code +"/dest/"+dest_code+"/date/"+date+"/apikey/"+api_key+"/"

r = requests.get(url=url)
res = r.json()


Name = []
Number = []
Arr_time = []
Dep_time = []
classes = []
class_level = []
seat_availability = []
frm = []
to = []
route = []

j = len(res['train'])
i=0
ticket="Sorry No Info Available at this time"

for i in range (0,j):
    Name.append(res['train'][i]['name'])
    frm.append(res['train'][i]['from']['code'])
    to.append(res['train'][i]['to']['code'])
    Number.append(res['train'][i]['number'])
    Arr_time.append(res['train'][i]['dest_arrival_time'])
    Dep_time.append(res['train'][i]['src_departure_time'])
    classes.append(res['train'][i]['classes'])

for i in range (0,j):
    print(str(i)+"- Date of journey : " + date+"-2016") 
    print("Train name : " + Name[i])
    print("Train number : " + Number[i])
    print("From : " + frm[i])
    print("Arrival time : " + Arr_time[i])
    print("to : " + to[i])
    print("Departure time : " + Dep_time[i])
    class_level = classes[i]
    for dic in class_level:
        if dic['class-code'] == level:
            print(level+" available or not : " + dic['available'])
    print("\n")
    
print("In which train you want to travel")
k=input()
print(Name[k]+" : ")
url = "http://api.railwayapi.com/route/train/"+Number[k]+"/apikey/"+api_key+"/"

r = requests.get(url=url)
res = r.json()
lengthOfRoute = len(res['route'])
i=0
for i in range (0,lengthOfRoute):
    route1 = []
    route1.append(res['route'][i]['fullname'])
    route1.append(res['route'][i]['code'])
    route.append(route1)
    
#print(route)

t=0
f=0
for i in range (0,lengthOfRoute):
    if route[i][1] == frm[k]:
        f=i
    if route[i][1] == to[k]:
        t=i

l=0

url = "http://api.railwayapi.com/check_seat/train/"+Number[k]+"/source/" +route[f][1]+ "/dest/" +route[t][1]+"/date/"+date+"-2016/class/"+level+"/quota/"+quota+"/apikey/"+api_key+"/"
r=requests.get(url=url)
result=r.json()

try:
    seat = result['availability'][0]['status']
    if seat[0:9] == "Available" or seat[0:3] == "RAC": 
        print("Seat_availability from "+route[f][1]+" to "+route[t][1]+ " is : " +seat)
    else:
        l=1
except:
    l=1 
if l== 1:
    url = "http://api.railwayapi.com/check_seat/train/"+Number[k]+"/source/" +route[f][1]+ "/dest/" +route[t-1][1]+"/date/"+date+"-2016/class/"+level+"/quota/"+quota+"/apikey/"+api_key+"/"
    r=requests.get(url=url)
    result=r.json()  
    try:
        seat = result['availability'][0]['status']
        if seat[0:9] == "Available" or seat[0:3] == "RAC": 
            print("Seat_availability from "+route[f][1]+" to "+route[t-1][1]+ " is : " +seat)
        else:
            l=2
    except:
        l=2
if l==2:
    url = "http://api.railwayapi.com/check_seat/train/"+Number[k]+"/source/" +route[f+1][1]+ "/dest/" +route[t][1]+"/date/"+date+"-2016/class/"+level+"/quota/"+quota+"/apikey/"+api_key+"/"
    r=requests.get(url=url)
    result=r.json()  
    try:
        seat = result['availability'][0]['status']
        if seat[0:9] == "Available" or seat[0:3] =="RAC":     
            print("Seat_availability from "+route[f+1][1]+" to "+route[t][1]+ " is : " +result['availability'][0]['status'])
        else:
            l=3
    except:
        l=3
if l==3:
    url = "http://api.railwayapi.com/check_seat/train/"+Number[k]+"/source/" +route[f+1][1]+ "/dest/" +route[t-1][1]+"/date/"+date+"-2016/class/"+level+"/quota/"+quota+"/apikey/"+api_key+"/"
    r=requests.get(url=url)
    result=r.json()  
    try:
        seat = result['availability'][0]['status']
        if seat[0:9] == "Available" or seat[0:3] =="RAC":     
            print("Seat_availability from "+route[f+1][1]+" to "+route[t-1][1]+ " is : " +result['availability'][0]['status'])
        else:
            l=4
    except:
        l=4
if l==4:
    url = "http://api.railwayapi.com/check_seat/train/"+Number[k]+"/source/" +route[f-1][1]+ "/dest/" +route[t][1]+"/date/"+date+"-2016/class/"+level+"/quota/"+quota+"/apikey/"+api_key+"/"
    r=requests.get(url=url)
    result=r.json()  
    try:
        seat = result['availability'][0]['status']
        if seat[0:9] == "Available" or seat[0:3] =="RAC":     
            print("Seat_availability from "+route[f-1][1]+" to "+route[t][1]+ " is : " +result['availability'][0]['status'])
        else:
            l=5
    except:
        l=5
if l==5:
    url = "http://api.railwayapi.com/check_seat/train/"+Number[k]+"/source/" +route[f-1][1]+ "/dest/" +route[t+1][1]+"/date/"+date+"-2016/class/"+level+"/quota/"+quota+"/apikey/"+api_key+"/"
    r=requests.get(url=url)
    result=r.json()
    try:
        seat = result['availability'][0]['status']
        if seat[0:9] == "Available" or seat[0:3] =="RAC":      
            print("Seat_availability from "+route[f-1][1]+" to "+route[t+1][1]+ " is : " +result['availability'][0]['status'])
        else:
            l=6
    except:
        print("Sorry there is no ticket available in this class")
if l==6:
    print("Sorry No ticket Available")
              
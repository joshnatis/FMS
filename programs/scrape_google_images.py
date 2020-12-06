import urllib.request
import urllib.parse
import requests

def getImgURL(query):
	url="https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
	headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64)"}
	req = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(req)
	text = response.read().decode("utf8")
	skip = text.find("<img") #googl logo
	start = text.find("<img", skip+1) #our image
	step1 = text.find("src", start) #start of src
	step2 = text.find(">", step1+1) #end of src
	return text[step1+5:step2-2] #im lazy

fin="OUTPUT.csv"
with open(fin, "r") as f:
	print(f.readline()[:-1], ", image")
	for line in f:
		comma1=line.find(",")
		comma2=line.find(",", comma1+1)
		name=line[comma1+1:comma2]
		foodid=line[0:comma1]
	        img=getImgURL(urllib.parse.quote_plus(name))
		print(line[:-1] + "," + img)
